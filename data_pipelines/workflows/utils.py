def get_outcome_modules(studies):
    outcome_modules = []
    for study in studies:
        if (
            "ResultsSection" in study["Study"]
            and "OutcomeMeasuresModule" in study["Study"]["ResultsSection"]
        ):
            outcome_modules.append(
                study["Study"]["ResultsSection"]["OutcomeMeasuresModule"]
            )
            continue

        identification_module = study["Study"]["ProtocolSection"][
            "IdentificationModule"
        ]
        if "OfficialTitle" in identification_module:
            study_title = identification_module["OfficialTitle"]
        else:
            study_title = identification_module["BriefTitle"]
        print("No Results: ", study_title)

    return outcome_modules
