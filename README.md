Web Scrapper initialy created to scrap the "Quinto Andar" page, a Brazilian Real State company.
The page uses tipical React-Cards, so it's easy to get and extract data from each card.

The basically functionality are described next:
1) I'd add a field to select the page to scrap, but for now only "5 Andar" is available;
2) Then the user need to paste the base URL which the scrapper will use, the check button is used to confirm if the scrapper could access the URL, returning the total number of results (cards) for that URL;
3) User can select which fields will be scrap and added to the output.csv file;
4) I'd add entry to select the maximum number of entries to scrap, since the page may result in large amount of entries;
5) Finally user can choose the name of file to be generated;
6) The scrapper operate headless, so the user only need to wait until it finish, which will pop a warning window;
7) The scrapper will scrap all rendered cards, then look for a button at the bottom of the page to "Show more" results;
8) It will do this until either the máx entries number is reached, or if the button isn't found (so it reached the end of that page);
9) At last, a .csv file is generated in the projects folder, the data is saved in every iteraction (avoiding data loss due app crashs);
10) A try/caught block is used to prevent app to crash if some field is not found;
