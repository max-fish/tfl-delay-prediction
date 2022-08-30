const config = {
    endpoint: "https://tfl-bus-approaches.documents.azure.com:443/",
    key: "hDiWUFl6St3SjZmxfYBy7NbFoQO1FmSMPiF3FjXFq653mC2o7HvJ0MWh7jB4XOziSb8xBVLFaAUsLF303rIGXw==",
    databaseId: "Tasks",
    containerId: "Items",
    partitionKey: { kind: "Hash", paths: ["/category"] }
  };
  
export default config;