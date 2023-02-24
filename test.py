@app.get(ROOT_URL + "/getInvoiceWKMaster&InvoiceWKDetail/{urlCondition}")
async def searchInvoiceWKMaster(
    request: Request,
    urlCondition: str,
    db: Session = Depends(get_db),
):
    # get query condition
    dictCondition = convert_url_condition_to_dict(urlCondition)
    date_condition = dict(filter(lambda x: "Date" in x[0], dictCondition.items()))
    status_condition = dict(filter(lambda x: "Status" in x[0], dictCondition.items()))
    newDictCondition = dict(
        filter(
            lambda x: "Date" not in x[0] and "Status" not in x[0], dictCondition.items()
        )
    )
    pprint(newDictCondition)

    # -------------------------- get data from db --------------------------
    # init CRUD
    crudInvoiceWKMaster = CRUD(db, InvoiceWKMasterDBModel)
    crudInvoiceWKDetail = CRUD(db, InvoiceWKDetailDBModel)

    # get InvoiceWKDetail data from db
    InvoiceWKDetailDataList = crudInvoiceWKDetail.get_with_condition(newDictCondition)
    pprint(InvoiceWKDetailDataList)
    WKMasterIDList = [
        InvoiceWKDetailData.WKMasterID
        for InvoiceWKDetailData in InvoiceWKDetailDataList
    ]
    pprint(WKMasterIDList)
    # get InvoiceWKMaster data from db
    InvoiceWKMasterDataList = crudInvoiceWKMaster.get_value_if_in_a_list(
        InvoiceWKMasterDBModel.WKMasterID, WKMasterIDList
    )
    if status_condition:
        if isinstance(status_condition["Status"], str):
            InvoiceWKMasterDataList = [
                InvoiceWKMasterData
                for InvoiceWKMasterData in InvoiceWKMasterDataList
                if InvoiceWKMasterData.Status == status_condition["Status"]
            ]
        else:
            InvoiceWKMasterDataList = [
                InvoiceWKMasterData
                for InvoiceWKMasterData in InvoiceWKMasterDataList
                if InvoiceWKMasterData.Status in status_condition["Status"]
            ]
    if date_condition:
        key = list(date_condition.keys())[0]
        col_name = key.replace("range", "")
        if date_condition[key]["gte"] == date_condition[key]["lte"]:
            date_condition[key]["lte"] = date_condition[key]["lte"][:10] + " 23:59:59"
        InvoiceWKMasterDataList = [
            InvoiceWKMasterData
            for InvoiceWKMasterData in InvoiceWKMasterDataList
            if date_condition[key]["gte"]
            <= orm_to_dict(InvoiceWKMasterData)[col_name]
            <= date_condition[key]["lte"]
        ]

    # generate result
    getResult = []
    for InvoiceWKMasterData in InvoiceWKMasterDataList:
        InvoiceWKDetailData = list(
            filter(
                lambda x: x.WKMasterID == InvoiceWKMasterData.WKMasterID,
                InvoiceWKDetailDataList,
            )
        )[0]
        getResult.append(
            {
                "InvoiceWKMaster": InvoiceWKMasterData,
                "InvoiceWKDetail": InvoiceWKDetailData,
            }
        )

    return getResult
