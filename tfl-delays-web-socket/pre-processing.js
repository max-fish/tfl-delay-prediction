const removeOutdatedPredictions = (arrivalPredictions) => {
    return arrivalPredictions.filter((prediction) => prediction['operationType'] !== 2)
}

const generateTableName = (prediction) => {
    const lineName = prediction['lineName'];
    const direction = prediction['direction'];

    const tableName = "ArrPred".concat(lineName, direction);
    return tableName;
};



export { removeOutdatedPredictions, generateTableName };