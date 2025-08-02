from typing import List

from cv.model.cert import Cert


def convert_to_table(certs: List[Cert]):
    return [
        [
            cert.title,
            cert.organization,
            cert.date,
        ]
        for cert in certs
    ]


professional_certs = [
    Cert(
        "Introduction to PyKX",
        "KX",
        "2025-01",
    ),
    Cert("KDB+/Q Developer Level 3", "KX", "2024-09", highlight="KDB+/Q"),
    Cert(
        "KDB+/Q Developer Level 2",
        "KX",
        "2024-07",
        highlight="KDB+/Q",
    ),
    Cert(
        "KDB+/Q Developer Level 1",
        "KX",
        "2024-06",
        highlight="KDB+/Q",
    ),
    Cert(
        "Learning Kubernetes",
        "LinkedIn Learning",
        "2024-06",
    ),
    Cert(
        "SE100: Responsive Web Development",
        "Heicoders Academy",
        "2023-12",
        highlight="Web Development",
    ),
    Cert(
        "Certified Scrum Developer (CSD)",
        "Scrum Alliance",
        "2023-10",
    ),
    Cert(
        "Building Transformer-Based Natural Language Processing Applications",
        "NVIDIA Deep Learning Institute",
        "2020-09",
    ),
    Cert(
        "Google Analytics for Beginners",
        "Google Analytics Academy",
        "2020-07",
    ),
    Cert(
        "Design Patterns",
        "NobleProg",
        "2020-04",
    ),
    Cert(
        "AWS Cloud Practitioner Essentials",
        "AWS",
        "2019-08",
    ),
    Cert(
        "Extracting Business Value through Data Analytics",
        "SMU Academy",
        "2018-09",
    ),
    Cert(
        "Developer Training for Spark and Hadoop",
        "Cloudera",
        "2018-08",
        highlight="Spark and Hadoop",
    ),
]


skill_certs = [
    Cert(
        "Italian, Beginner",
        "inlingua School of Languages",
        "2023-09",
    ),
    Cert(
        "Climbing, Level One",
        "Singapore National Climbing Standards",
        "2023-09",
    ),
    Cert(
        "Typing Certificate, Platinum (119wpm, 100% accuracy)",
        "Ratatype",
        "2017-07",
    ),
    Cert(
        "Diving, Open Water Diver",
        "Professional Association of Diving Instructors",
        "2017-03",
    ),
    Cert(
        "Kayaking, Two Star",
        "Singapore Canoe Federation	",
        "2016-01",
    ),
    Cert(
        "LCM Electronic Organ, Grade 8 Distinction",
        "University of West London",
        "2012-09",
    ),
    Cert(
        "Mental Arithmetic, Class 2",
        "International Abacus Mathematics Association",
        "2008-11",
    ),
    Cert(
        "Swimming, Gold",
        "Singapore Sports Council",
        "2006-03",
    ),
]
