def create_baselines_table_helper(studies: typing.List[dict]) -> pd.DataFrame:
    df = {
        'study': [],
        'group_id': [],
        'base': [],
        'class': [],
        'category': [],
        'param_type': [],
        'dispersion_type': [],
        'unit': [],
        'value': [],
        'spread': [],
        'upper': [],
        'lower': []
    }

    for study in studies:
        study_id = study['Study']['ProtocolSection']['IdentificationModule']['NCTId']
        measures = study['Study']['ResultsSection']['BaselineCharacteristicsModule'].get('BaselineMeasureList', {'BaselineMeasure': []})['BaselineMeasure']

        for measure in measures:
            classes = measure.get('BaselineClassList', {'BaselineClass': []})['BaselineClass']

            for clss in classes:
                categories = clss.get('BaselineCategoryList', {'BaselineCategory': []})['BaselineCategory']

                for category in categories:
                    measurements = category.get('BaselineMeasurementList', {'BaselineMeasurement': []})['BaselineMeasurement']

                    for measurement in measurements:
                        df['study'].append(study_id)
                        df['group_id'].append(measurement.get('BaselineMeasurementGroupId', 'NA'))
                        df['base'].append(measure.get('BaselineMeasureTitle', 'NA'))
                        df['class'].append(clss.get('BaselineClassTitle', 'NA'))
                        df['category'].append(category.get('BaselineCategoryTitle', 'NA'))
                        df['param_type'].append(measure.get('BaselineMeasureParamType', 'NA'))
                        df['dispersion_type'].append(measure.get('BaselineMeasureDispersionType', 'NA'))
                        df['unit'].append(measure.get('BaselineMeasureUnitOfMeasure', 'NA'))
                        df['value'].append(measurement.get('BaselineMeasurementValue', 'NA'))
                        df['spread'].append(measurement.get('BaselineMeasurementSpread', 'NA'))
                        df['upper'].append(measurement.get('BaselineMeasurementUpperLimit', 'NA'))
                        df['lower'].append(measurement.get('BaselineMeasurementLowerLimit', 'NA'))

    return df


def clean_baselines_table(baselines_table: pd.DataFrame) -> pd.None:
    baselines_table['base'] = baselines_table['base'].fillna('NA')
    baselines_table['clss'] = baselines_table['clss'].fillna('NA')
    baselines_table['category'] = baselines_table['category'].fillna('NA')
    baselines_table['param_type'] = baselines_table['param_type'].fillna('NA')
    baselines_table['unit'] = baselines_table['unit'].fillna('NA')
    baselines_table['type'] = baselines_table['type'].fillna('OTHER')
    baselines_table['sub_type'] = baselines_table['sub_type'].fillna('NA')
    baselines_table['dispersion'] = baselines_table['dispersion'].str.replace(' ','_').str.replace('-','_')
    baselines_table['param_type'] = baselines_table['param_type'].str.upper().str.replace(' ', '_')

    return baselines_table.drop(columns=['group_id'])


def store_pre_cleaned_baselines_table_pkl(baselines_table: pd.DataFrame) -> None:
    baselines_table.to_pickle(DATA_PATH + 'pre_cleaned_baselines_table.pkl')


def create_baselines_table() -> pd.DataFrame:
    baselines_table_dfs = []
    directory = DATA_PATH + 'clinical_trials/'

    for studies_data_pickle_file in os.listdir(directory):
        studies_file = os.path.join(directory, studies_data_pickle_file)
        print(f"Deserializing {studies_file}")

        with open(studies_file, 'rb') as f:
            studies_data = pickle.load(f)
            baselines_table_df = create_baselines_table_helper(studies=studies_data)
            baselines_table_dfs.append(baselines_table_df)

    studies_table = pd.concat(baselines_table_dfs).reset_index(drop=True)
    return studies_table


def baselines_workflow():
    baselines_table = create_baselines_table()
    store_pre_cleaned_baselines_table_pkl(baselines_table)
    baselines_table = clean_baselines_table(baselines_table)
    upload_to_db(baselines_table)


if __name__ == '__main__':
    baselines_workflow()
