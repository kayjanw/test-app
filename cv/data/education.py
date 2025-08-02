from typing import List

from cv.model.cert import Cert


def convert_to_table(certs: List[Cert]):
    return [
        [
            cert.title,
            cert.organization,
            cert.link_button,
        ]
        for cert in certs
    ]


coursera_ai = [
    Cert(
        "Advanced Machine Learning on Google Cloud (5-course specialization)",
        "Google Cloud",
        "https://www.coursera.org/account/accomplishments/specialization/GKGNXBAJBE2P",
    ),
    Cert(
        "Deep Learning (5-course specialization)",
        "deeplearning.ai",
        "https://www.coursera.org/account/accomplishments/specialization/JNXU8C3XNHHF",
    ),
    Cert(
        "TensorFlow in Practice (4-course specialization)",
        "deeplearning.ai",
        "https://www.coursera.org/account/accomplishments/specialization/ULFDP3LB3DVV",
    ),
    Cert(
        "Natural Language Processing (4-course specialization)",
        "deeplearning.ai",
        "https://www.coursera.org/account/accomplishments/specialization/9FTHRDTF36U5",
    ),
    Cert(
        "Machine Learning Engineering for Production (MLOps) (4-course specialization)",
        "deeplearning.ai",
        "https://www.coursera.org/account/accomplishments/specialization/KM9Z5TA4WB85",
    ),
    Cert(
        "AI for Everyone",
        "deeplearning.ai",
        "https://www.coursera.org/account/accomplishments/certificate/8R3E3SA7FZVQ",
    ),
    Cert(
        "AI for Medical Treatment",
        "deeplearning.ai",
        "https://www.coursera.org/account/accomplishments/certificate/WV2VXQFXNBVY",
    ),
    Cert(
        "Generative AI with Large Language Models",
        "deeplearning.ai",
        "https://www.coursera.org/account/accomplishments/certificate/9ZCU98Y3HH5U",
    ),
    Cert(
        "Natural Language Processing",
        "National Research University Higher School of Economics",
        "https://www.coursera.org/account/accomplishments/certificate/984GCLL5LGQA",
    ),
    Cert(
        "Sentiment Analysis with Deep Learning using BERT",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/BHVBXE6YU98D",
        highlight="Sentiment Analysis",
    ),
    Cert(
        "Named Entity Recognition using LSTMs with Keras",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/BGN9GTRC9V6H",
    ),
    Cert(
        "Anomaly Detection in Time Series Data with Keras",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/8KNJZPFUSD9Y",
        highlight="Anomaly Detection",
    ),
]
coursera_big_data = [
    Cert(
        "Introduction to Big Data",
        "University of California San Diego",
        "https://www.coursera.org/account/accomplishments/certificate/YMSL632YH4GB",
    ),
    Cert(
        "Hadoop Platform and Application Framework",
        "University of California San Diego",
        "https://www.coursera.org/account/accomplishments/certificate/BS9PJK9QFK5W",
        highlight="Hadoop",
    ),
    Cert(
        "Big Data Essentials: HDFS, MapReduce and Spark RDD (with Honors)",
        "Yandex",
        "https://www.coursera.org/account/accomplishments/certificate/KEL6QFPUPY47",
    ),
    Cert(
        "Big Data Analysis: Hive, Spark SQL, DataFrames and GraphFrames (with Honors)",
        "Yandex",
        "https://www.coursera.org/account/accomplishments/certificate/MUNMZD2AWZJ7",
    ),
    Cert(
        "Big Data Applications: Machine Learning at Scale",
        "Yandex",
        "https://www.coursera.org/account/accomplishments/certificate/W6G25WEMHZQE",
    ),
    Cert(
        "Big Data Applications: Real-Time Streaming",
        "Yandex",
        "https://www.coursera.org/account/accomplishments/certificate/QEWCWLD4W69Z",
    ),
]
coursera_coding = [
    Cert(
        "Python for Everybody (5-course specialization)",
        "University of Michigan",
        "https://www.coursera.org/account/accomplishments/specialization/BHPET73W22AL",
    ),
    Cert(
        "Introduction to Scripting in Python (4-course specialization)",
        "Rice University",
        "https://www.coursera.org/account/accomplishments/specialization/FDRGRPX3CC4W",
    ),
    Cert(
        "Java Programming and Software Engineering Fundamentals (5-course specialization)",
        "Duke University",
        "https://www.coursera.org/account/accomplishments/specialization/J7JAH5BYRPWF",
    ),
    Cert(
        "Software Design and Architecture (4-course specialization)",
        "University of Alberta",
        "https://www.coursera.org/account/accomplishments/specialization/SCPF827UF684",
    ),
    Cert(
        "Programming with Google Go (3-course specialization)",
        "University of California Irvine",
        "https://www.coursera.org/account/accomplishments/specialization/353MHAETH6SJ",
    ),
    Cert(
        "Introduction to Golang - Basic Concepts",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/KWVQBRNVDSDL",
    ),
    Cert(
        "Concepts in Golang - Loops, decision statements and function",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/JL5CDKB9P8P2",
    ),
    Cert(
        "R Programming",
        "John Hopkins University",
        "https://www.coursera.org/account/accomplishments/certificate/RG9KZL4SNSLJ",
    ),
    Cert(
        "Advanced R Programming",
        "John Hopkins University",
        "https://www.coursera.org/account/accomplishments/certificate/57J84F78R97M",
    ),
    Cert(
        "Effective Programming in Scala",
        "École Polytechnique Fédérale de Lausanne (EPFL)",
        "https://www.coursera.org/account/accomplishments/certificate/B6T54CTB73AF",
    ),
    Cert(
        "Spring - Ecosystem and Core",
        "LearnQuest",
        "https://www.coursera.org/account/accomplishments/certificate/AGPBTHRVG778",
    ),
    Cert(
        "Introduction to Structured Query Language (SQL)",
        "University of Michigan",
        "https://www.coursera.org/account/accomplishments/certificate/DGPKLV3F4GDR",
    ),
    Cert(
        "SQL for Data Science",
        "University of California, Davis",
        "https://www.coursera.org/account/accomplishments/certificate/KGF7279CBEB3",
    ),
    Cert(
        "Intermediate PostgreSQL",
        "University of Michigan",
        "https://www.coursera.org/account/accomplishments/certificate/PJUT68JS6CXB",
    ),
    Cert(
        "TypeScript - Learning the fundamentals",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/RLKTQYM2K5WF",
    ),
    Cert(
        "TypeScript Variables and Data Types",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/XEQUBCZCZCLA",
    ),
    Cert(
        "TypeScript Operators",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/BLRTBYSH2P7D",
    ),
    Cert(
        "TypeScript Arrays",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/BXQKECPNFR4P",
    ),
    Cert(
        "TypeScript String Properties and Methods",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/DW44XTXYLM9Q",
    ),
    Cert(
        "TypeScript Control Structures",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/YDFU5QJLWMD9",
    ),
    Cert(
        "Typescript in React: Higher Order Components",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/JJK7H7M6EKU2",
    ),
    Cert(
        "Introduction to Bash Shell Scripting",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/M82E582ACQSU",
    ),
    Cert(
        "Version Control with Git",
        "Atlassian",
        "https://www.coursera.org/account/accomplishments/certificate/UGAJSYWP9J3J",
    ),
    Cert(
        "The Unix Workbench",
        "Johns Hopkins University",
        "https://www.coursera.org/account/accomplishments/certificate/Q5WVCPNCWUET",
    ),
]
coursera_ds = [
    Cert(
        "Applied Data Science with Python (5-course specialization)",
        "University of Michigan",
        "https://www.coursera.org/account/accomplishments/specialization/FZTSGNFCHZAL",
    ),
    Cert(
        "Advanced Business Analytics (5-course specialization)",
        "University of Colorado Boulder",
        "https://www.coursera.org/account/accomplishments/specialization/63LDWB945XDM",
    ),
    Cert(
        "An Intuitive Introduction to Probability",
        "Univerity of Zurich",
        "https://www.coursera.org/account/accomplishments/certificate/2GBB94PQRLQV",
    ),
    Cert(
        "Basic Statistics",
        "University of Amsterdam",
        "https://www.coursera.org/account/accomplishments/certificate/RK6UPM6FM5UZ",
    ),
    Cert(
        "Inferential Statistics",
        "University of Amsterdam",
        "https://www.coursera.org/account/accomplishments/certificate/87NYRUQPLQRV",
    ),
    Cert(
        "Statistical Inference",
        "John Hopkins University",
        "https://www.coursera.org/account/accomplishments/certificate/J9QQ2T7PG4VE",
    ),
    Cert(
        "Improving Your Statistical Inferences",
        "Eindhoven University of Technology",
        "https://www.coursera.org/account/accomplishments/certificate/CUDYXQ7BXVE8",
    ),
    Cert(
        "Data Visualization",
        "University of Illinois at Urbana-Champaign",
        "https://www.coursera.org/account/accomplishments/certificate/ST38U6379NSN",
    ),
    Cert(
        "Pattern Discovery in Data Mining",
        "University of Illinois at Urbana-Champaign",
        "https://www.coursera.org/account/accomplishments/certificate/PQFWT76KHXMW",
    ),
    Cert(
        "Computer Vision Basics",
        "University of Buffalo & The State University of New York",
        "https://www.coursera.org/account/accomplishments/certificate/WKJQFGV6ASTQ",
    ),
    Cert(
        "Image Processing, Features & Segmentation",
        "University of Buffalo & The State University of New York",
        "https://www.coursera.org/account/accomplishments/certificate/EV8EP55X9CLW",
    ),
    Cert(
        "Practical Time Series Analysis",
        "The State University of New York",
        "https://www.coursera.org/account/accomplishments/certificate/5AC2J6QA2DY3",
        highlight="Time Series",
    ),
]
coursera_finance = [
    Cert(
        "Investment and Portfolio Management (5-course specialization)",
        "Rice University",
        "https://www.coursera.org/account/accomplishments/specialization/WBKDA55PP22N",
    ),
    Cert(
        "Risk Management (4-course specialization)",
        "New York Institute of Finance",
        "https://www.coursera.org/account/accomplishments/specialization/TZ2SBK93CSHX",
    ),
    Cert(
        "Finance for Non-Financial Professionals",
        "University of California, Irvine",
        "https://www.coursera.org/account/accomplishments/certificate/VHQQXQ76SHP5",
    ),
]
coursera_se = [
    Cert(
        "Cloud Application Development Foundations (4-course specialization)",
        "IBM",
        "https://www.coursera.org/account/accomplishments/specialization/WFUJK9EG75AG",
    ),
    Cert(
        "Modern Application Development with .NET on AWS (3-course specialization)",
        "Amazon Web Services",
        "https://www.coursera.org/account/accomplishments/specialization/85Z4NX6WRNR7",
    ),
    Cert(
        "Scrum Master Certification (4-course specialization)",
        "LearnQuest",
        "https://www.coursera.org/account/accomplishments/specialization/4RTEGTZNBKWV",
    ),
    Cert(
        "Six Sigma Yellow Belt (4-course specialization)",
        "University System of Georgia",
        "https://www.coursera.org/account/accomplishments/specialization/KT5UYBZPSBKK",
    ),
    Cert(
        "AWS S3 Basics",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/MCQEKSDQJ7Z2",
    ),
    Cert(
        "Create and run a .NET Core console app in Linux using docker",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/2WTLMD6SMDXV",
    ),
]
coursera_others = [
    Cert(
        "Algorithms (4-course specialization)",
        "Stanford University",
        "https://www.coursera.org/account/accomplishments/specialization/3722CHEPCCBL",
    ),
    Cert(
        "Blockchain (4-course specialization)",
        "University at Buffalo",
        "https://www.coursera.org/account/accomplishments/specialization/GY4BUQB46M8V",
    ),
    Cert(
        "Usable Security",
        "University of Maryland, College Park",
        "https://www.coursera.org/account/accomplishments/certificate/R973H9L4BS8C",
    ),
    Cert(
        "Software Security",
        "University of Maryland, College Park",
        "https://www.coursera.org/account/accomplishments/certificate/9MXT3LEYCL2Q",
    ),
    Cert(
        "Project Management: Creating the WBS",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/N3LGV4NNZW7N",
    ),
]
datacamp_ds = [
    Cert(
        "Machine Learning Fundamentals with Python (4-course track)",
        "Track",
        "https://www.datacamp.com/statement-of-accomplishment/track/a964873c9dccc9e846a56e359abe4e31c9e460cf",
    ),
    Cert(
        "Machine Learning for Everyone",
        "Course",
        "https://www.datacamp.com/statement-of-accomplishment/course/b53932af06b654da619f9b3b40b450052147e975",
    ),
    Cert(
        "Machine Learning for Time Series Data in Python",
        "Course",
        "https://www.datacamp.com/statement-of-accomplishment/course/b53932af06b654da619f9b3b40b450052147e975",
    ),
    Cert(
        "Introduction to Deep Learning in Python",
        "Course",
        "https://www.datacamp.com/statement-of-accomplishment/course/adb779e424170e92352d5e22e0b9aa18a10cb399",
    ),
    Cert(
        "Introduction to PySpark",
        "Course",
        "https://www.datacamp.com/statement-of-accomplishment/course/ed417c8adcc34cc205e78a34b9bee5384c6ec4c5",
        highlight="PySpark",
    ),
    Cert(
        "Feature Engineering with PySpark",
        "Course",
        "https://www.datacamp.com/statement-of-accomplishment/course/ddd4fddeb091d9c7f45a847460c6816aa6407cf8",
        highlight="PySpark",
    ),
]
datacamp_coding = [
    Cert(
        "Python Programmer (15-course track)",
        "Career Track",
        "https://www.datacamp.com/statement-of-accomplishment/track/d5f82ebabc68e0c1616ed1702b7a90caa27fdcc8",
    ),
    Cert(
        "Python Programming (6-course track)",
        "Track",
        "https://www.datacamp.com/statement-of-accomplishment/track/e0af9978b5b5bead5c391db0beacbab3f2670473",
    ),
    Cert(
        "Working with the Class System in Python",
        "Course",
        "https://www.datacamp.com/statement-of-accomplishment/course/c464bdecc7337da1bb8669d0f260d332b323d086",
    ),
    Cert(
        "Creating Robust Workflows in Python",
        "Course",
        "https://www.datacamp.com/statement-of-accomplishment/course/11a3ee596a0e4fe006feb7739d603b3f9f78069a",
    ),
    Cert(
        "Introduction to Scala",
        "Course",
        "https://www.datacamp.com/statement-of-accomplishment/course/9aaa94d628ff5316b4cf988de9a82fb961c899e5",
    ),
]

coursera_data = [
    (coursera_ai, "Artificial Intelligence"),
    (coursera_big_data, "Big Data"),
    (coursera_coding, "Coding Best Practices"),
    (coursera_ds, "Data Science"),
    (coursera_finance, "Finance"),
    (coursera_se, "Software Engineering"),
    (coursera_others, "Others"),
]

datacamp_data = [
    (datacamp_coding, "Coding Best Practices"),
    (datacamp_ds, "Data Science"),
]
