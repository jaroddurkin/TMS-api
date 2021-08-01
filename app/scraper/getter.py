import scraper.objectMapper

def getSectionsForClassAndTerm(code, term):
    rawData = scraper.objectMapper.createClassList(code, term)
    objects = scraper.objectMapper.makeObjects(rawData)

    return objects
