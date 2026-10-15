from statistics import mean


def calculate_statistics(patients, waiting_patients=None):
    ages = [patient["age"] for patient in patients]

    return {
        "total_patients": len(patients),
        "average_age": round(mean(ages), 1) if ages else 0,
        "under_18": sum(age < 18 for age in ages),
        "age_60_plus": sum(age >= 60 for age in ages),
        "waiting_patients": (
            len(patients) if waiting_patients is None else waiting_patients
        ),
    }