import scraper.objectMapper

def getSectionsForClassAndTerm(code, term):
    rawData = scraper.objectMapper.createClassList(code, term)
    objects = scraper.objectMapper.makeObjects(rawData, False)

    return objects

def getSectionDetailedForClassAndTerm(code, term):
    rawData = scraper.objectMapper.createClassList(code, term)
    objects = scraper.objectMapper.makeObjects(rawData, True)

    return objects
