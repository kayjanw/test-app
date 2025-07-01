from typing import List

import dash_mantine_components as dmc
from dash import html


def create_scrollable_area(data: List[List[str]], columns: List[str], **kwargs):
    table_kwargs = dict(
        withTableBorder=False,
        withColumnBorders=False,
        withRowBorders=False,
        highlightOnHover=True,
        horizontalSpacing="xs",
        verticalSpacing="xs",
    )
    table_kwargs = {**table_kwargs, **kwargs}

    return dmc.TableScrollContainer(
        dmc.Table(children=create_course_table(data, columns), **table_kwargs),
        maxHeight=400,
        minWidth=600,
        type="scrollarea",
    )


def create_course_table(data: List[List[str]], columns: List[str]):
    return [
        html.Thead(html.Tr([html.Th(col) for col in columns])),
        html.Tbody(
            [
                html.Tr(
                    [
                        html.Td(_data[0]),
                        html.Td(_data[1]),
                    ]
                    + (
                        [
                            html.Td(
                                html.A(
                                    dmc.Button("Details", size="md"),
                                    href=_data[2],
                                    target="_blank",
                                )
                            )
                            if _data[2].startswith("http")
                            else html.Td(_data[2])
                        ]
                        if len(columns) == 3
                        else []
                    )
                )
                for _data in data
            ]
        ),
    ]


coursera_ai = [
    [
        "Advanced Machine Learning on Google Cloud (5-course specialization)",
        "Google Cloud",
        "https://www.coursera.org/account/accomplishments/specialization/GKGNXBAJBE2P",
    ],
    [
        "Deep Learning (5-course specialization)",
        "deeplearning.ai",
        "https://www.coursera.org/account/accomplishments/specialization/JNXU8C3XNHHF",
    ],
    [
        "TensorFlow in Practice (4-course specialization)",
        "deeplearning.ai",
        "https://www.coursera.org/account/accomplishments/specialization/ULFDP3LB3DVV",
    ],
    [
        "Natural Language Processing (4-course specialization)",
        "deeplearning.ai",
        "https://www.coursera.org/account/accomplishments/specialization/9FTHRDTF36U5",
    ],
    [
        "Machine Learning Engineering for Production (MLOps) (4-course specialization)",
        "deeplearning.ai",
        "https://www.coursera.org/account/accomplishments/specialization/KM9Z5TA4WB85",
    ],
    [
        "AI for Everyone",
        "deeplearning.ai",
        "https://www.coursera.org/account/accomplishments/certificate/8R3E3SA7FZVQ",
    ],
    [
        "AI for Medical Treatment",
        "deeplearning.ai",
        "https://www.coursera.org/account/accomplishments/certificate/WV2VXQFXNBVY",
    ],
    [
        "Generative AI with Large Language Models",
        "deeplearning.ai",
        "https://www.coursera.org/account/accomplishments/certificate/9ZCU98Y3HH5U",
    ],
    [
        "Natural Language Processing",
        "National Research University Higher School of Economics",
        "https://www.coursera.org/account/accomplishments/certificate/984GCLL5LGQA",
    ],
    [
        "Sentiment Analysis with Deep Learning using BERT",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/BHVBXE6YU98D",
    ],
    [
        "Named Entity Recognition using LSTMs with Keras",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/BGN9GTRC9V6H",
    ],
    [
        "Anomaly Detection in Time Series Data with Keras",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/8KNJZPFUSD9Y",
    ],
]
coursera_big_data = [
    [
        "Introduction to Big Data",
        "University of California San Diego",
        "https://www.coursera.org/account/accomplishments/certificate/YMSL632YH4GB",
    ],
    [
        "Hadoop Platform and Application Framework",
        "University of California San Diego",
        "https://www.coursera.org/account/accomplishments/certificate/BS9PJK9QFK5W",
    ],
    [
        "Big Data Essentials: HDFS, MapReduce and Spark RDD (with Honors)",
        "Yandex",
        "https://www.coursera.org/account/accomplishments/certificate/KEL6QFPUPY47",
    ],
    [
        "Big Data Analysis: Hive, Spark SQL, DataFrames and GraphFrames (with Honors)",
        "Yandex",
        "https://www.coursera.org/account/accomplishments/certificate/MUNMZD2AWZJ7",
    ],
    [
        "Big Data Applications: Machine Learning at Scale",
        "Yandex",
        "https://www.coursera.org/account/accomplishments/certificate/W6G25WEMHZQE",
    ],
    [
        "Big Data Applications: Real-Time Streaming",
        "Yandex",
        "https://www.coursera.org/account/accomplishments/certificate/QEWCWLD4W69Z",
    ],
]


coursera_coding = [
    [
        "Python for Everybody (5-course specialization)",
        "University of Michigan",
        "https://www.coursera.org/account/accomplishments/specialization/BHPET73W22AL",
    ],
    [
        "Introduction to Scripting in Python (4-course specialization)",
        "Rice University",
        "https://www.coursera.org/account/accomplishments/specialization/FDRGRPX3CC4W",
    ],
    [
        "Java Programming and Software Engineering Fundamentals (5-course specialization)",
        "Duke University",
        "https://www.coursera.org/account/accomplishments/specialization/J7JAH5BYRPWF",
    ],
    [
        "Software Design and Architecture (4-course specialization)",
        "University of Alberta",
        "https://www.coursera.org/account/accomplishments/specialization/SCPF827UF684",
    ],
    [
        "Programming with Google Go (3-course specialization)",
        "University of California Irvine",
        "https://www.coursera.org/account/accomplishments/specialization/353MHAETH6SJ",
    ],
    [
        "Introduction to Golang - Basic Concepts",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/KWVQBRNVDSDL",
    ],
    [
        "Concepts in Golang - Loops, decision statements and function",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/JL5CDKB9P8P2",
    ],
    [
        "R Programming",
        "John Hopkins University",
        "https://www.coursera.org/account/accomplishments/certificate/RG9KZL4SNSLJ",
    ],
    [
        "Advanced R Programming",
        "John Hopkins University",
        "https://www.coursera.org/account/accomplishments/certificate/57J84F78R97M",
    ],
    [
        "Effective Programming in Scala",
        "École Polytechnique Fédérale de Lausanne (EPFL)",
        "https://www.coursera.org/account/accomplishments/certificate/B6T54CTB73AF",
    ],
    [
        "Spring - Ecosystem and Core",
        "LearnQuest",
        "https://www.coursera.org/account/accomplishments/certificate/AGPBTHRVG778",
    ],
    [
        "Introduction to Structured Query Language (SQL)",
        "University of Michigan",
        "https://www.coursera.org/account/accomplishments/certificate/DGPKLV3F4GDR",
    ],
    [
        "SQL for Data Science",
        "University of California, Davis",
        "https://www.coursera.org/account/accomplishments/certificate/KGF7279CBEB3",
    ],
    [
        "Intermediate PostgreSQL",
        "University of Michigan",
        "https://www.coursera.org/account/accomplishments/certificate/PJUT68JS6CXB",
    ],
    [
        "TypeScript - Learning the fundamentals",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/RLKTQYM2K5WF",
    ],
    [
        "TypeScript Variables and Data Types",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/XEQUBCZCZCLA",
    ],
    [
        "TypeScript Operators",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/BLRTBYSH2P7D",
    ],
    [
        "TypeScript Arrays",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/BXQKECPNFR4P",
    ],
    [
        "TypeScript String Properties and Methods",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/DW44XTXYLM9Q",
    ],
    [
        "TypeScript Control Structures",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/YDFU5QJLWMD9",
    ],
    [
        "Typescript in React: Higher Order Components",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/JJK7H7M6EKU2",
    ],
    [
        "Introduction to Bash Shell Scripting",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/M82E582ACQSU",
    ],
    [
        "Version Control with Git",
        "Atlassian",
        "https://www.coursera.org/account/accomplishments/certificate/UGAJSYWP9J3J",
    ],
    [
        "The Unix Workbench",
        "Johns Hopkins University",
        "https://www.coursera.org/account/accomplishments/certificate/Q5WVCPNCWUET",
    ],
]

coursera_ds = [
    [
        "Applied Data Science with Python (5-course specialization)",
        "University of Michigan",
        "https://www.coursera.org/account/accomplishments/specialization/FZTSGNFCHZAL",
    ],
    [
        "Advanced Business Analytics (5-course specialization)",
        "University of Colorado Boulder",
        "https://www.coursera.org/account/accomplishments/specialization/63LDWB945XDM",
    ],
    [
        "An Intuitive Introduction to Probability",
        "Univerity of Zurich",
        "https://www.coursera.org/account/accomplishments/certificate/2GBB94PQRLQV",
    ],
    [
        "Basic Statistics",
        "University of Amsterdam",
        "https://www.coursera.org/account/accomplishments/certificate/RK6UPM6FM5UZ",
    ],
    [
        "Inferential Statistics",
        "University of Amsterdam",
        "https://www.coursera.org/account/accomplishments/certificate/87NYRUQPLQRV",
    ],
    [
        "Statistical Inference",
        "John Hopkins University",
        "https://www.coursera.org/account/accomplishments/certificate/J9QQ2T7PG4VE",
    ],
    [
        "Improving Your Statistical Inferences",
        "Eindhoven University of Technology",
        "https://www.coursera.org/account/accomplishments/certificate/CUDYXQ7BXVE8",
    ],
    [
        "Data Visualization",
        "University of Illinois at Urbana-Champaign",
        "https://www.coursera.org/account/accomplishments/certificate/ST38U6379NSN",
    ],
    [
        "Pattern Discovery in Data Mining",
        "University of Illinois at Urbana-Champaign",
        "https://www.coursera.org/account/accomplishments/certificate/PQFWT76KHXMW",
    ],
    [
        "Computer Vision Basics",
        "University of Buffalo & The State University of New York",
        "https://www.coursera.org/account/accomplishments/certificate/WKJQFGV6ASTQ",
    ],
    [
        "Image Processing, Features & Segmentation",
        "University of Buffalo & The State University of New York",
        "https://www.coursera.org/account/accomplishments/certificate/EV8EP55X9CLW",
    ],
    [
        "Practical Time Series Analysis",
        "The State University of New York",
        "https://www.coursera.org/account/accomplishments/certificate/5AC2J6QA2DY3",
    ],
]

coursera_finance = [
    [
        "Investment and Portfolio Management (5-course specialization)",
        "Rice University",
        "https://www.coursera.org/account/accomplishments/specialization/WBKDA55PP22N",
    ],
    [
        "Risk Management (4-course specialization)",
        "New York Institute of Finance",
        "https://www.coursera.org/account/accomplishments/specialization/TZ2SBK93CSHX",
    ],
    [
        "Finance for Non-Financial Professionals",
        "University of California, Irvine",
        "https://www.coursera.org/account/accomplishments/certificate/VHQQXQ76SHP5",
    ],
]

coursera_se = [
    [
        "Cloud Application Development Foundations (4-course specialization)",
        "IBM",
        "https://www.coursera.org/account/accomplishments/specialization/WFUJK9EG75AG",
    ],
    [
        "Modern Application Development with .NET on AWS (3-course specialization)",
        "Amazon Web Services",
        "https://www.coursera.org/account/accomplishments/specialization/85Z4NX6WRNR7",
    ],
    [
        "Scrum Master Certification (4-course specialization)",
        "LearnQuest",
        "https://www.coursera.org/account/accomplishments/specialization/4RTEGTZNBKWV",
    ],
    [
        "Six Sigma Yellow Belt (4-course specialization)",
        "University System of Georgia",
        "https://www.coursera.org/account/accomplishments/specialization/KT5UYBZPSBKK",
    ],
    [
        "AWS S3 Basics",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/MCQEKSDQJ7Z2",
    ],
    [
        "Create and run a .NET Core console app in Linux using docker",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/2WTLMD6SMDXV",
    ],
]

coursera_others = [
    [
        "Algorithms (4-course specialization)",
        "Stanford University",
        "https://www.coursera.org/account/accomplishments/specialization/3722CHEPCCBL",
    ],
    [
        "Blockchain (4-course specialization)",
        "University at Buffalo",
        "https://www.coursera.org/account/accomplishments/specialization/GY4BUQB46M8V",
    ],
    [
        "Usable Security",
        "University of Maryland, College Park",
        "https://www.coursera.org/account/accomplishments/certificate/R973H9L4BS8C",
    ],
    [
        "Software Security",
        "University of Maryland, College Park",
        "https://www.coursera.org/account/accomplishments/certificate/9MXT3LEYCL2Q",
    ],
    [
        "Project Management: Creating the WBS",
        "Coursera Project Network",
        "https://www.coursera.org/account/accomplishments/certificate/N3LGV4NNZW7N",
    ],
]

datacamp_ds = [
    [
        "Machine Learning Fundamentals with Python (4-course track)",
        "Track",
        "https://www.datacamp.com/statement-of-accomplishment/track/a964873c9dccc9e846a56e359abe4e31c9e460cf",
    ],
    [
        "Machine Learning for Everyone",
        "Course",
        "https://www.datacamp.com/statement-of-accomplishment/course/b53932af06b654da619f9b3b40b450052147e975",
    ],
    [
        "Machine Learning for Time Series Data in Python",
        "Course",
        "https://www.datacamp.com/statement-of-accomplishment/course/b53932af06b654da619f9b3b40b450052147e975",
    ],
    [
        "Introduction to Deep Learning in Python",
        "Course",
        "https://www.datacamp.com/statement-of-accomplishment/course/adb779e424170e92352d5e22e0b9aa18a10cb399",
    ],
    [
        "Introduction to PySpark",
        "Course",
        "https://www.datacamp.com/statement-of-accomplishment/course/ed417c8adcc34cc205e78a34b9bee5384c6ec4c5",
    ],
    [
        "Feature Engineering with PySpark",
        "Course",
        "https://www.datacamp.com/statement-of-accomplishment/course/ddd4fddeb091d9c7f45a847460c6816aa6407cf8",
    ],
]

datacamp_coding = [
    [
        "Python Programmer (15-course track)",
        "Career Track",
        "https://www.datacamp.com/statement-of-accomplishment/track/d5f82ebabc68e0c1616ed1702b7a90caa27fdcc8",
    ],
    [
        "Python Programming (6-course track)",
        "Track",
        "https://www.datacamp.com/statement-of-accomplishment/track/e0af9978b5b5bead5c391db0beacbab3f2670473",
    ],
    [
        "Working with the Class System in Python",
        "Course",
        "https://www.datacamp.com/statement-of-accomplishment/course/c464bdecc7337da1bb8669d0f260d332b323d086",
    ],
    [
        "Creating Robust Workflows in Python",
        "Course",
        "https://www.datacamp.com/statement-of-accomplishment/course/11a3ee596a0e4fe006feb7739d603b3f9f78069a",
    ],
    [
        "Introduction to Scala",
        "Course",
        "https://www.datacamp.com/statement-of-accomplishment/course/9aaa94d628ff5316b4cf988de9a82fb961c899e5",
    ],
]

professional_certs = [
    [
        "Introduction to PyKX",
        "KX",
        "2025-01",
    ],
    [
        "KDB+/Q Developer Level 3",
        "KX",
        "2024-09",
    ],
    [
        "KDB+/Q Developer Level 2",
        "KX",
        "2024-07",
    ],
    [
        "KDB+/Q Developer Level 1",
        "KX",
        "2024-06",
    ],
    [
        "Learning Kubernetes",
        "LinkedIn Learning",
        "2024-06",
    ],
    [
        "SE100: Responsive Web Development",
        "Heicoders Academy",
        "2023-12",
    ],
    [
        "Certified Scrum Developer (CSD)",
        "Scrum Alliance",
        "2023-10",
    ],
    [
        "Building Transformer-Based Natural Language Processing Applications",
        "NVIDIA Deep Learning Institute",
        "2020-09",
    ],
    [
        "Google Analytics for Beginners",
        "Google Analytics Academy",
        "2020-07",
    ],
    [
        "Design Patterns",
        "NobleProg",
        "2020-04",
    ],
    [
        "AWS Cloud Practitioner Essentials",
        "AWS",
        "2019-08",
    ],
    [
        "Extracting Business Value through Data Analytics",
        "SMU Academy",
        "2018-09",
    ],
    [
        "Developer Training for Spark and Hadoop",
        "Cloudera",
        "2018-08",
    ],
]

skill_certs = [
    [
        "Italian, Beginner",
        "inlingua School of Languages",
        "2023-09",
    ],
    [
        "Climbing, Level One",
        "Singapore National Climbing Standards",
        "2023-09",
    ],
    [
        "Typing Certificate, Platinum (119wpm, 100% accuracy)",
        "Ratatype",
        "2017-07",
    ],
    [
        "Diving, Open Water Diver",
        "Professional Association of Diving Instructors",
        "2017-03",
    ],
    [
        "Kayaking, Two Star",
        "Singapore Canoe Federation	",
        "2016-01",
    ],
    [
        "LCM Electronic Organ, Grade 8 Distinction",
        "University of West London",
        "2012-09",
    ],
    [
        "Mental Arithmetic, Class 2",
        "International Abacus Mathematics Association",
        "2008-11",
    ],
    [
        "Swimming, Gold",
        "Singapore Sports Council",
        "2006-03",
    ],
]

books_read_leisure = [
    [
        "The Little Prince",
        "Antoine de Saint-Exupery",
        "Adventure",
    ],
    [
        "The Girl Who Saved the King of Sweden",
        "Jonas Jonasson",
        "Adventure, Satirical",
    ],
    [
        "The Hundred-Year-Old Man Who Climbed Out the Window and Disappeared",
        "Jonas Jonasson",
        "Adventure, Satirical",
    ],
    [
        "Hitman Anders and the Meaning of It All",
        "Jonas Jonasson",
        "Adventure, Satirical",
    ],
    [
        "Before the Coffee Gets Cold",
        "Toshikazu Kawaguchi",
        "Touching",
    ],
    [
        "Ikigai",
        "Francesc Miralles, Hector Garcia",
        "Inspiring",
    ],
    [
        "Ichigo Ichie",
        "Francesc Miralles, Hector Garcia",
        "Transformative",
    ],
]

books_read_self = [
    [
        "The Art of Thinking Clearly",
        "Rolf Dobelli",
        "★★★★★ Must read",
    ],
    [
        "Difficult Conversations",
        "Douglas Stone",
        "★★★★★ Learnt a lot",
    ],
    [
        "Crucial Conversations: Tools for Talking When Stakes are High",
        "Kerry Patterson, Joseph Grenny, Al Switzler, Ron McMillan",
        "★★★★★ Not very structured",
    ],
    [
        "The 21 Indispensable Qualities of a Leader",
        "John C. Maxwell",
        "★★★★☆ Insightful",
    ],
    [
        "Life Coaching: Change Your Life in 7 Days",
        "Eileen Mulligan",
        "★★★☆☆ Not comprehensive",
    ],
    [
        "Rules of Thinking",
        "Richard Templar",
        "★★★★☆ Interesting tips",
    ],
]

books_read_technical = [
    [
        "Software Teaming: A Mob Programming, Whole-Team Approach",
        "Woody Zuill, Kevin Meadows",
        "★★★★☆ Practical",
    ],
    [
        "Head First Software Architecture",
        "Mark Richards, Neal Ford, Raju Gandhi",
        "★★★★☆ Easy to digest",
    ],
    [
        "The Pragmatic Programmer",
        "David Thomas, Andrew Hunt",
        "★★★★★ Awesome tips and reminder",
    ],
    [
        "The Manager's Path: A Guide for Tech Leaders Navigating Growth and Change",
        "Camille Fournier",
        "★★★★★ Insightful",
    ],
    [
        "Getting Started In Technical Analysis",
        "Jack D. Schwager",
        "★★★☆☆ A little dry",
    ],
    [
        "Refactoring, Second Edition",
        "Martin Fowler",
        "★★★☆☆ Straightforward",
    ],
]

books_reading_leisure = [
    [
        "The Accidental Further Adventures of the Hundred-Year-Old Man",
        "Jonas Jonasson",
    ],
    [
        "Butter",
        "Asako Yuzuki",
    ],
]

books_reading_self = []

books_reading_technical = [
    ["Software Engineering at Google", "Titus Winters, Tom Manshreck, Hyrum Wright"]
]


sample = [
    [
        "",
        "",
        "",
    ],
]
