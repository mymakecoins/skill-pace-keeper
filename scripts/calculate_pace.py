#!/usr/bin/env python3
"""
calculate_pace.py - Calculadora de velocidade e cadencia para a skill pace-keeper.
Gera metricas determinísticas de throughput diário, pontos de esforço e prazos.
"""

import argparse
import datetime
import json
import sys


def parse_date(date_str: str) -> datetime.date:
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        try:
            return datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError:
            raise argparse.ArgumentTypeError(f"Formato de data inválido: {date_str}. Use AAAA-MM-DD ou DD/MM/AAAA.")


def get_default_brazilian_holidays(year: int) -> set:
    holidays = {
        datetime.date(year, 1, 1),   # Confraternização Universal
        datetime.date(year, 4, 21),  # Tiradentes
        datetime.date(year, 5, 1),   # Dia do Trabalho
        datetime.date(year, 9, 7),   # Independência
        datetime.date(year, 10, 12), # Nossa Senhora Aparecida
        datetime.date(year, 11, 2),  # Finados
        datetime.date(year, 11, 15), # Proclamação da República
        datetime.date(year, 11, 20), # Consciência Negra
        datetime.date(year, 12, 25), # Natal
    }
    return holidays


def count_days(start_date: datetime.date, target_date: datetime.date, holidays: set, work_on_holidays: bool = False, work_on_weekends: bool = False):
    if target_date < start_date:
        raise ValueError("Data-alvo não pode ser anterior à data inicial.")

    total_calendar_days = (target_date - start_date).days
    current = start_date
    business_days = 0
    weekend_days = 0
    holiday_days = 0

    while current < target_date:
        is_weekend = current.weekday() >= 5
        is_holiday = current in holidays

        if is_weekend:
            weekend_days += 1
            if work_on_weekends:
                business_days += 1
        elif is_holiday:
            holiday_days += 1
            if work_on_holidays:
                business_days += 1
        else:
            business_days += 1

        current += datetime.timedelta(days=1)

    return {
        "calendar_days": total_calendar_days,
        "business_days": business_days,
        "weekend_days": weekend_days,
        "holiday_days": holiday_days
    }


def main():
    parser = argparse.ArgumentParser(description="Calculadora de ritmo de desenvolvimento (pace-keeper)")
    parser.add_argument("--target-date", "-t", required=True, type=parse_date, help="Data limite de entrega (AAAA-MM-DD ou DD/MM/AAAA)")
    parser.add_argument("--start-date", "-s", type=parse_date, default=datetime.date.today(), help="Data inicial / atual (default: hoje)")
    parser.add_argument("--tasks-p", type=int, default=0, help="Quantidade de tarefas tamanho P (peso 1)")
    parser.add_argument("--tasks-m", type=int, default=0, help="Quantidade de tarefas tamanho M (peso 2)")
    parser.add_argument("--tasks-g", type=int, default=0, help="Quantidade de tarefas tamanho G (peso 4)")
    parser.add_argument("--tasks-other", type=int, default=0, help="Quantidade de tarefas sem tamanho definido (peso médio 2)")
    parser.add_argument("--atomic-tasks", type=int, default=0, help="Quantidade estimada de subtarefas atômicas (ex: tasks.md)")
    parser.add_argument("--buffer-days", type=float, default=1.0, help="Dias reservados para homologação/staging/buffer final (default: 1.0)")
    parser.add_argument("--work-on-holidays", action="store_true", help="Considerar feriados como dias úteis")
    parser.add_argument("--work-on-weekends", action="store_true", help="Considerar finais de semana como dias úteis")
    parser.add_argument("--custom-holidays", nargs="*", type=parse_date, help="Lista de feriados adicionais (AAAA-MM-DD)")
    parser.add_argument("--analysts", type=int, default=1, help="Quantidade de analistas atuando no projeto (default: 1)")
    parser.add_argument("--json", action="store_true", help="Saída em formato JSON")

    args = parser.parse_args()

    analysts = max(1, args.analysts)
    holidays = get_default_brazilian_holidays(args.start_date.year)
    if args.target_date.year != args.start_date.year:
        holidays.update(get_default_brazilian_holidays(args.target_date.year))
    if args.custom_holidays:
        holidays.update(args.custom_holidays)

    day_stats = count_days(
        start_date=args.start_date,
        target_date=args.target_date,
        holidays=holidays,
        work_on_holidays=args.work_on_holidays,
        work_on_weekends=args.work_on_weekends
    )

    total_tasks = args.tasks_p + args.tasks_m + args.tasks_g + args.tasks_other
    total_points = (args.tasks_p * 1) + (args.tasks_m * 2) + (args.tasks_g * 4) + (args.tasks_other * 2)

    net_business_days = max(0.5, day_stats["business_days"] - args.buffer_days)
    calendar_days = max(1, day_stats["calendar_days"])

    tasks_per_business_day = total_tasks / net_business_days if total_tasks > 0 else 0
    points_per_business_day = total_points / net_business_days if total_points > 0 else 0
    atomic_per_business_day = args.atomic_tasks / net_business_days if args.atomic_tasks > 0 else 0

    tasks_per_calendar_day = total_tasks / calendar_days if total_tasks > 0 else 0
    points_per_calendar_day = total_points / calendar_days if total_points > 0 else 0

    tasks_per_analyst = tasks_per_business_day / analysts
    points_per_analyst = points_per_business_day / analysts
    atomic_per_analyst = atomic_per_business_day / analysts

    result = {
        "start_date": args.start_date.isoformat(),
        "target_date": args.target_date.isoformat(),
        "calendar_days": day_stats["calendar_days"],
        "raw_business_days": day_stats["business_days"],
        "buffer_days": args.buffer_days,
        "net_business_days": round(net_business_days, 2),
        "holidays_count": day_stats["holiday_days"],
        "weekend_days": day_stats["weekend_days"],
        "analysts": analysts,
        "total_tasks": total_tasks,
        "breakdown": {
            "p": args.tasks_p,
            "m": args.tasks_m,
            "g": args.tasks_g,
            "other": args.tasks_other
        },
        "total_points": total_points,
        "atomic_tasks": args.atomic_tasks,
        "required_pace": {
            "team": {
                "tasks_per_net_business_day": round(tasks_per_business_day, 2),
                "points_per_net_business_day": round(points_per_business_day, 2),
                "atomic_tasks_per_net_business_day": round(atomic_per_business_day, 2),
                "tasks_per_calendar_day": round(tasks_per_calendar_day, 2),
                "points_per_calendar_day": round(points_per_calendar_day, 2)
            },
            "per_analyst": {
                "tasks_per_net_business_day": round(tasks_per_analyst, 2),
                "points_per_net_business_day": round(points_per_analyst, 2),
                "atomic_tasks_per_net_business_day": round(atomic_per_analyst, 2)
            }
        }
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("=== RELATORIO DE RITMO (PACE-KEEPER) ===")
        print(f"Periodo: {args.start_date} ate {args.target_date}")
        print(f"Dias corridos: {day_stats['calendar_days']} dias")
        print(f"Dias uteis brutos: {day_stats['business_days']} dias (feriados: {day_stats['holiday_days']}, fins de semana: {day_stats['weekend_days']})")
        print(f"Buffer reservado para release/homologacao: {args.buffer_days} dias")
        print(f"Dias uteis liquidos de desenvolvimento: {net_business_days:.1f} dias")
        print(f"Equipe: {analysts} analista(s)")
        print("---")
        print(f"Escopo total: {total_tasks} tarefas macro ({args.tasks_p} P, {args.tasks_m} M, {args.tasks_g} G, {args.tasks_other} sem tamanho)")
        print(f"Total de pontos de esforco: {total_points} pts")
        if args.atomic_tasks > 0:
            print(f"Subtarefas atomicas estimadas: {args.atomic_tasks} subtarefas")
        print("---")
        print("VELOCIDADE NECESSARIA (TIME TOTAL):")
        print(f"- Tarefas por dia util liquido: {tasks_per_business_day:.2f} tarefas/dia")
        print(f"- Pontos por dia util liquido: {points_per_business_day:.2f} pts/dia")
        if args.atomic_tasks > 0:
            print(f"- Subtarefas atomicas por dia util liquido: {atomic_per_business_day:.2f} subtarefas/dia")
        print(f"- Tarefas por dia corrido: {tasks_per_calendar_day:.2f} tarefas/dia")
        print(f"- Pontos por dia corrido: {points_per_calendar_day:.2f} pts/dia")
        if analysts > 1:
            print("---")
            print(f"VELOCIDADE INDIVIDUAL POR ANALISTA ({analysts} analistas):")
            print(f"- Tarefas por analista/dia: {tasks_per_analyst:.2f} tarefas/analista/dia")
            print(f"- Pontos por analista/dia: {points_per_analyst:.2f} pts/analista/dia")
            if args.atomic_tasks > 0:
                print(f"- Subtarefas por analista/dia: {atomic_per_analyst:.2f} subtarefas/analista/dia")


if __name__ == "__main__":
    main()
