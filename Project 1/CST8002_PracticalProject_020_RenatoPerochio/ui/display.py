DIVIDER = "=" * 55

def show_records(records, author):
    print(f"\n{DIVIDER}")
    print(f"  Loaded {len(records)} record(s) from dataset")
    print(f"  CST8002 Practical Project 1  |  Author: {author}")
    print(DIVIDER)

    for i, record in enumerate(records):
        print(f"\n  --- RECORD {i + 1} ---")
        print(f" Year:                  {record.year}")
        print(f" Species:               {record.species}")
        print(f" Common Name:           {record.common_name}")
        print(f" Study Site:            {record.study_site}")
        print(f" Associated Community:  {record.associated_community}")
        print(f" Latitude:              {record.lat}")
        print(f" Longitude:             {record.long}")
        print(f" delta13C:              {record.delta13C}")
        print(f" delta13Cc:             {record.delta13Cc}")
        print(f" delta15N:              {record.delta15N}")
        print(f" delta15Nc:             {record.delta15Nc}")
        print(f" TP:                    {record.tp}")
        print(f" CN:                    {record.cn}")
        print(f" Astaxanthin(mg/kg):    {record.astaxanthin}")
        print(f" Canthaxanthin(mg/kg):  {record.canthaxanthin}")
        print(f" Retinol(mg/kg):        {record.retinol}")

    print(f"\n{DIVIDER}")
    print(f" End of Records List  |  Total Records: {len(records)}")
    print(DIVIDER)