// tests/selenium/search.test.js

const { Builder, By, until } = require("selenium-webdriver");
const assert = require("assert");

// Décrire le groupe de tests "Search Functionality"
describe("Search Functionality", () => {
  let driver;

  // Avant tous les tests, configurer le WebDriver Selenium (ajuster le navigateur si nécessaire, par exemple 'chrome', 'firefox')
  beforeAll(async () => {
    driver = await new Builder().forBrowser("chrome").build();
  });

  // Après tous les tests, fermer le navigateur
  afterAll(async () => {
    await driver.quit();
  });

  // Le test doit effectuer une recherche et afficher les résultats sur SearchResultPage
  it("should perform a search and display results on SearchResultPage", async () => {
    // Naviguer vers votre SearchPage
    await driver.get("http://localhost:3000/search"); // Remplacer par l'URL réelle de votre SearchPage

    // Trouver le champ de saisie de recherche par son attribut placeholder
    const searchInput = await driver.findElement(
      By.css('input[placeholder="Rechercher un article"]')
    );

    // Entrer une requête de recherche
    const searchQuery = "dummy";
    await searchInput.sendKeys(searchQuery);

    // Trouver le bouton de recherche par le contenu textuel
    const searchButton = await driver.findElement(
      By.xpath('//button[text()="Search"]')
    );

    // Cliquer sur le bouton de recherche pour lancer la recherche
    await searchButton.click();

    // Attendre la redirection vers SearchResultPage
    await driver.wait(until.urlContains("result"), 5000);

    // Vérifier si l'URL contient la requête de recherche
    const currentUrl = await driver.getCurrentUrl();
    assert(
      currentUrl.includes(`q=${encodeURIComponent(searchQuery)}`),
      "Search query not found in the URL."
    );

    // Attendre que les résultats de recherche ou le message "Pas de résultat" soient affichés
    await driver.wait(
      until.elementLocated(By.className("result-container")),
      5000
    );

    // Vérifier s'il y a des résultats de recherche ou le message "Pas de résultat"
    const searchResults = await driver.findElements(
      By.className("result-container")
    );
    const noResultsMessage = await driver.findElements(
      By.xpath('//p[text()="Pas de résultat"]')
    );

    assert(
      searchResults.length > 0 || noResultsMessage.length > 0,
      "No search results found."
    );
  });
});
