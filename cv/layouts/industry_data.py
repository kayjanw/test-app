import dash_mantine_components as dmc
from dash import dcc, html

from cv.layouts.helper import bullet_point

squarepoint_details = [
    "Quantative Developer, Squarepoint",
    "Commodities and Other Mandates | May 2024 - Present",
    "tabler:briefcase-2",
    [
        bullet_point(
            "✔️",
            dmc.Highlight(
                "Developed and maintained in-house Python packages to automate report publishing to DocViewer and "
                "Confluence, standardising the reports and reducing workload for Quant Researchers",
                highlight="automate report publishing",
                style={"fontSize": "inherit"},
            ),
        ),
        bullet_point(
            "✔️",
            html.P(
                "Managed and migrated codebases, CI/CD pipelines, Prefect jobs, and API endpoints, collaborating with "
                "a global team of 15+ developers"
            ),
        ),
        bullet_point(
            "✔️",
            html.P(
                "Led sprint management and support efforts, addressing queries and resolving issues for Quant "
                "Researchers"
            ),
        ),
        bullet_point(
            "🎖️️️",
            dmc.Highlight(
                "Reduced latency of minutely alpha publication from 26s to 6s",
                highlight="Reduced latency",
                style={"fontSize": "inherit"},
            ),
        ),
    ],
    "industry-sqp",
]


gic_details = [
    "Senior Software Developer, GIC",
    "Technology Group, Business Partner and Solutions, Total Portfolio | Jul 2022 - May 2024",
    "tabler:briefcase-2",
    [
        bullet_point(
            "✔️",
            dmc.Highlight(
                "Enhanced departments' capability of computing risk, performance, and exposure metrics for "
                "top-of-the-house reporting by developing in-house Python packages, computation engines, and backend "
                "APIs",
                highlight=[
                    "computing risk, performance, and exposure metrics",
                    "Python packages, computation engines, and backend APIs",
                ],
                style={"fontSize": "inherit"},
            ),
        ),
        bullet_point(
            "✔️",
            html.P(
                "Drove project progress by orchestrating coordination between developers and end users, gathering "
                "requirements from end users and scoping the work, ensuring timely delivery ahead of milestones"
            ),
        ),
        bullet_point(
            "🎖️",
            dmc.Highlight(
                "Ideated and developed open-source Python package for working with tree data structures, with over 100 "
                "GitHub stars to date",
                highlight="open-source Python package",
                style={"fontSize": "inherit"},
            ),
        ),
    ],
    "industry-gic",
]


dbs_details = [
    "Data Scientist / Machine Learning Engineer, DBS",
    "Transformation Group, Analytics Centre of Excellence (ACOE) | Aug 2018 - Jul 2022",
    "tabler:briefcase-2",
    [
        bullet_point(
            "✔️",
            html.P(
                "Built, deployed, and monitored ML pipeline and performed system integration testing to predict and "
                "address customers' needs prior to call"
            ),
        ),
        bullet_point(
            "✔️",
            dmc.Highlight(
                "Initiated and single-handedly improved data and feature engineering pipeline architecture to "
                "standardize processing, reduce resource wastage, and increase scalability, resulting in time savings "
                "of over 35 hours",
                highlight="time savings of over 35 hours",
                style={"fontSize": "inherit"},
            ),
        ),
        bullet_point(
            "🎖️",
            html.P(
                "Published in IJCNN 2020 Personalized Digital Customer Services for Consumer Banking Call Centre using "
                "Neural Networks"
            ),
        ),
        bullet_point(
            "✔️",
            dmc.Highlight(
                "Developed forecasting methods for time series, involving EDA, processing, models, and pipelines, "
                "subsequently packaged and deployed it to DBS internal server using Jenkins",
                highlight="forecasting methods for time series",
                style={"fontSize": "inherit"},
            ),
        ),
        bullet_point(
            "✔️",
            dmc.Highlight(
                "Implemented end-to-end forecasting and anomaly detection workflows with CBG, IBG teams across SG, HK "
                "teams to forecast trade volume, CASA balances and transactions, metrics related to cards onboarding "
                "and more",
                highlight="forecasting and anomaly detection workflows",
                style={"fontSize": "inherit"},
            ),
        ),
        bullet_point(
            "✔️",
            html.P(
                "Independently created and launched an enterprise-wide web application encompassing time series "
                "forecasting methods using Dash and Plotly, and deployed it using Jenkins and OpenShift",
            ),
        ),
        bullet_point(
            "🎖️",
            html.P(
                "Launched 2 forecasting e-learning courses for bank-wide staff, collaborating with Culture and "
                "Curriculum team, and have over 1500 user completions to date"
            ),
        ),
        bullet_point(
            "✔️",
            dmc.Highlight(
                "Deployed end-to-end anomaly detection and forecasting pipeline on QlikView dashboard within 5 months "
                "of project inception, making it the first AI-embedded Control Tower within the bank",
                highlight=["first AI-embedded Control Tower within the bank"],
                style={"fontSize": "inherit"},
            ),
        ),
        bullet_point(
            "🎖️",
            html.P(
                "Published in ACM 2022 Improving Operational Efficiency through Predicting Credit Card Application "
                "Turnaround Time with Index-based Encoding"
            ),
        ),
        bullet_point(
            "✔️",
            dmc.Highlight(
                "Experience in classification, regression, time series, NLP, and clustering machine learning methods "
                "through various projects",
                highlight=[
                    "classification, regression, time series, NLP, and clustering"
                ],
                style={"fontSize": "inherit"},
            ),
        ),
        bullet_point(
            "🎖️",
            html.P(
                "4x Spot Award recipient for 2021 Feb, Jun, Oct, and 2022 Apr for exemplary work performance"
            ),
        ),
        bullet_point(
            "🎖️",
            html.P(
                "Star Award recipient for first half of 2021 for exemplary work performance"
            ),
        ),
        bullet_point(
            "🎖️",
            html.P("Completed over 100 Coursera courses within the span of 3.5 years"),
        ),
        bullet_point(
            "🎖️",
            html.P(
                "Represented Musicians Interest Group in DBS Dinner and Dance 2019 and 2021, playing keyboard in a "
                "live band"
            ),
        ),
    ],
    "industry-dbs",
]

kpmg_details = [
    "Management Intern, KPMG",
    "Advisory, IT Assurance and Security (ITAS) | May 2017 - Jul 2017",
    "tabler:school",
    [
        bullet_point(
            "✔️",
            dmc.Highlight(
                "Review of IT processes and controls over logical and physical access, password management, user "
                "account management, audit logging, program change management, system development lifecycle, computer "
                "operations etc., governing data integrity,confidentiality and availability",
                highlight="Review of IT processes and controls",
                style={"fontSize": "inherit"},
            ),
        ),
        bullet_point(
            "✔️",
            html.P(
                "Attended professional training courses in assurance reporting and SAP modules"
            ),
        ),
        bullet_point(
            "✔️",
            html.P(
                "Exposed to banking risk management, custody, data analytics, global financial services, prime "
                "brokerage, private equity, securitization, treasury and various frameworks"
            ),
        ),
        bullet_point(
            "🎖️️️",
            html.P(
                "Represented Topaz (Team Advisory) in KPMG Sports Carnival 2017, clinching first place in Cheerleading "
                "and second place in Touch Rugby, assisting Topaz to secure Overall Champion"
            ),
        ),
    ],
    "industry-kpmg",
]

db_details = [
    "Campus Ambassador, Deutsche Bank",
    "Aug 2016 - Aug 2017",
    "tabler:school",
    [
        bullet_point(
            "✔️",
            html.P(
                "Assist in building networks within campus and with the employer brand and recruitment team at "
                "Deutsche Bank"
            ),
        ),
        bullet_point(
            "✔️",
            html.P(
                "Influence and shape Deutsche Bank's on-campus marketing activities and recruitment strategies"
            ),
        ),
    ],
    "industry-db",
]


squarepoint_content_details = html.Div(
    [
        html.H5("Quantative Developer, Squarepoint"),
        html.H6("Commodities and Other Mandates | May 2024 - Present"),
        html.Br(),
        html.Details(
            [
                html.Summary("Technical", className="p-summary"),
                dcc.Markdown(
                    """
        > ✔️ Developed and maintained in-house Python packages to automate report publishing to
            DocViewer and Confluence, standardising the reports and reducing workload for Quant
            Researchers

        > ✔️ Managed and migrated codebases, CI/CD pipelines, Prefect jobs, and API endpoints,
            collaborating with a global team of 15+ developers

        > ✔️ Led sprint management and support efforts, addressing queries and resolving issues for
            Quant Researchers

        > 🎖️️ Reduced latency of minutely alpha publication from 26s to 6s
        """
                ),
            ],
            title="Expand for details",
        ),
        html.Br(),
    ]
)


gic_content_details = html.Div(
    [
        html.H5("Senior Software Developer, GIC"),
        html.H6(
            "Technology Group, Business Partner and Solutions, Total Portfolio | Jul 2022 - May 2024"
        ),
        html.Br(),
        html.Details(
            [
                html.Summary("Enterprise Risk", className="p-summary"),
                dcc.Markdown(
                    """
                    > ✔️ Enhanced departments' capability of computing risk, performance, and exposure metrics
                        for top-of-the-house reporting by developing in-house Python packages, computation
                        engines, and backend APIs

                    > ✔️ Drove project progress by orchestrating coordination between developers and end users,
                        gathering requirements from end users and scoping the work, ensuring timely delivery
                        ahead of milestones

                    > 🎖️ Ideated and developed open-source Python package for working with tree data structures,
                        with over 100 GitHub stars to date
                    """
                ),
            ],
            title="Expand for details",
        ),
        html.Br(),
    ],
    className="custom-div-instruction custom-div-left",
)

dbs_content_details = html.Div(
    [
        html.H5("Data Scientist / Machine Learning Engineer, DBS"),
        html.H6(
            "Transformation Group, Analytics Centre of Excellence (ACOE) | Aug 2018 - Jul 2022"
        ),
        html.Br(),
        html.Details(
            [
                html.Summary(
                    "CBO Call Centre Call Reduction Project (CCTR)",
                    className="p-summary",
                ),
                dcc.Markdown(
                    """
                    > ✔️ Built, deployed, and monitored ML pipeline and performed system integration testing to
                        predict and address customers' needs prior to call

                    > ✔️ Initiated and single-handedly improved data and feature engineering pipeline
                        architecture to standardize processing, reduce resource wastage, and increase scalability,
                        resulting in time savings of over 35 hours

                    > ✔️ Delivered data analysis and insights to various stakeholders in accordance to business
                        requirements to track model performance, support experimentation, and drive decision making

                    > ✔️ Performed predictive analysis with rule-based model as a real-time use case using
                        Adobe IBMB clickstream data

                    > 🎖️ Published in IJCNN 2020 Personalized Digital Customer Services for Consumer Banking
                        Call Centre using Neural Networks
                    """
                ),
            ],
            title="Expand for details",
        ),
        html.Details(
            [
                html.Summary(
                    "Time Series Forecast Reusable Asset (FORA)",
                    className="p-summary",
                ),
                dcc.Markdown(
                    """
                    > ✔️ Developed forecasting methods for time series, involving EDA, processing, models, and
                        pipelines, subsequently packaged and deployed it to DBS internal server using Jenkins

                    > ✔️ Implemented end-to-end forecasting and anomaly detection workflows with CBG, IBG teams
                        across SG, HK teams to forecast trade volume, CASA balances and transactions, metrics
                        related to cards onboarding and more

                    > ✔️ Held workshops, demonstrations, project presentations, and code walkthroughs to
                        business and technical teams from SG, CN, TW, HK and ID

                    > ✔️ Independently created and launched an enterprise-wide web application encompassing
                        time series forecasting methods using Dash and Plotly, and deployed it using Jenkins and
                        OpenShift

                    > 🎖️ Launched 2 forecasting e-learning courses for bank-wide staff, collaborating with
                        Culture and Curriculum team, and have over 1500 user completions to date

                    > 🎖️ Voted top Reusable Asset (RA) in RA Learning Festival 2020
                    """
                ),
            ],
            title="Expand for details",
        ),
        html.Details(
            [
                html.Summary("CBO Cards MTJ Project", className="p-summary"),
                dcc.Markdown(
                    """
                    > ✔️ Developed end-to-end anomaly detection and forecasting pipeline to predict metrics
                        related to card onboarding journey

                    > ✔️ Deployed solution on QlikView dashboard within 5 months of project inception, making it
                        the first AI-embedded Control Tower within the bank

                    > 🎖️ Published in ACM 2022 Improving Operational Efficiency through Predicting Credit Card
                        Application Turnaround Time with Index-based Encoding
                    """
                ),
            ],
            title="Expand for details",
        ),
        html.Details(
            [
                html.Summary("CBG Mortgage Project", className="p-summary"),
                dcc.Markdown(
                    """
                    > ✔️ Developed end-to-end ML solution for mortgage pricing to predict customers' reprice rate

                    > ✔️ Improved existing data pipeline architecture, resulting in 85% time savings

                    > ✔️ Managed project deliverables, deployment plans, and drove project to deployment in 6
                        months
                    """
                ),
            ],
            title="Expand for details",
        ),
        html.Details(
            [
                html.Summary("Audit Summarization Project", className="p-summary"),
                dcc.Markdown(
                    """
                    > ✔️ Performed ideation, experimentation, evaluation, and benchmarking of different models
                        for NLP summarization task for Audit issues

                    > ✔️ Tested and deployed API solution on GPU in UAT
                    """
                ),
            ],
            title="Expand for details",
        ),
        html.Details(
            [
                html.Summary("T&M FX Project", className="p-summary"),
                dcc.Markdown(
                    """
                    > ✔️ Developed pipelines to automate campaign analysis, standardizing processing across 2
                        campaigns and 3 types of campaign analysis
                    """
                ),
            ],
            title="Expand for details",
        ),
        html.Details(
            [
                html.Summary("Feature Mart Reusable Asset", className="p-summary"),
                dcc.Markdown(
                    """
                    > ✔️ Formalized and implemented Feature Mart which automates feature creation for CBG data
                        and standardizes processing required
                    """
                ),
            ],
            title="Expand for details",
        ),
        html.Details(
            [
                html.Summary("Other Projects", className="p-summary"),
                dcc.Markdown(
                    """
                    > ✔️ Performed email clustering using different text cleaning and embedding methods and "
                            "machine learning models

                    > ✔️ Implemented best practices workflow in multiple projects by setting up integration "
                            "testing of codes and enabling distributed processing

                    > ✔️ Have experience with Kedro-style pipelines
                    """
                ),
            ],
            title="Expand for details",
        ),
        html.Details(
            [
                html.Summary("Others", className="p-summary"),
                dcc.Markdown(
                    """
                    > 🎖️ 4x Spot Award recipient for 2021 Feb, Jun, Oct, and 2022 Apr for exemplary work performance

                    > 🎖️ Star Award recipient for first half of 2021 for exemplary work performance

                    > 🎖️ Second most active Coursera user, based on course completion, in the company in 2018

                    > 🎖️ Completed over 100 Coursera courses within the span of 3.5 years

                    > 🎖️ Represented Musicians Interest Group in DBS Dinner and Dance 2019 and 2021, playing
                        keyboard in a live band
                    """
                ),
            ],
            title="Expand for details",
        ),
    ]
)


kpmg_content_details = html.Div(
    [
        html.H5("Management Intern, KPMG"),
        html.H6("Advisory, IT Assurance and Security (ITAS) | May 2017 - Jul 2017"),
        html.Br(),
        html.Details(
            [
                html.Summary("Advisory", className="p-summary"),
                dcc.Markdown(
                    """
                            > ✔️ Review of IT processes and controls over logical and physical access, password
                                management, user account management, audit logging, program change management, system
                                development lifecycle, computer operations etc., governing data integrity,
                                confidentiality and availability

                            > ✔️ Attended professional training courses in assurance reporting and SAP modules

                            > ✔️ Exposed to banking risk management, custody, data analytics, global financial services,
                            prime brokerage, private equity, securitization, treasury and various frameworks

                            > 🎖️️ Represented Topaz (Team Advisory) in KPMG Sports Carnival 2017, clinching first place
                            in Cheerleading and second place in Touch Rugby, assisting Topaz to secure Overall Champion
                            """
                ),
            ],
            title="Expand for details",
        ),
        html.Br(),
    ],
    className="custom-div-instruction custom-div-left",
)

db_content_details = html.Div(
    [
        html.H5("Campus Ambassador, Deutsche Bank"),
        html.H6("Aug 2016 - Aug 2017"),
        html.Br(),
        html.Details(
            [
                html.Summary("Ambassador", className="p-summary"),
                dcc.Markdown(
                    """
                            > ✔️ Assist in building networks within campus and with the employer brand and recruitment
                                team at Deutsche Bank

                            > ✔️ Influence and shape Deutsche Bank's on-campus marketing activities and recruitment
                                strategies
                            """
                ),
            ],
            title="Expand for details",
        ),
        html.Br(),
    ],
    className="custom-div-instruction custom-div-left",
)

industry_content_details = [
    squarepoint_content_details,
    gic_content_details,
    dbs_content_details,
    kpmg_content_details,
    db_content_details,
]
