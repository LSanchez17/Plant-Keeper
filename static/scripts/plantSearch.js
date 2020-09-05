/*
*  This searches through an API for plants based on user input
*  Makes a call to second API for plants with no image
*/
const PLANT_API_KEY_REMOVE_ME = '7c-JHovj1mUW2xTvrfm30aMUZ1W0T9GM0p0wncztwRA';
const URL = '/api/plants/search';

class SearchPlantAPI{
    constructor(){
        this.APIKEY = PLANT_API_KEY_REMOVE_ME;
        this.BaseUrl = URL;
    }

    async GetPlant(query){
        let response = await axios.get(this.BaseUrl, {
            params: {
                'q':query
            }
        })

        return response.data;
    }
}

let searchPlant = document.querySelector('#searchPlant');
let appendResults = document.querySelector('#plant-search-output');

searchPlant.addEventListener('submit', (e) => {
    e.preventDefault();

    let query = document.querySelector('#searchQuery').value;
    let newSearch = new SearchPlantAPI();
    let dataOfSearch = newSearch.GetPlant(query);

    console.log(dataOfSearch);

    // let test = document.createElement('p');
    // test.innerText = searchResult;

    // console.log(test)
    // appendResults.append(test);

})