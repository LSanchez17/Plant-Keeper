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

async function imageAPI(query){
    let response = await axios.get('/api/plants/images', {
        params:{
            'q': query
        }
    })
    return response.data
}

const filterData = (largeObj, query) => {
    /*
    *   Returns an array of just objects with properties to use
    *   [{n}...{n+m}]
    */
    let plantArray = [];
    query = query.toUpperCase();

    for(let eachObj in largeObj){
        //step through returned call
        if(largeObj.hasOwnProperty('data')){
        //We only want to run through the first object here
        // console.log(largeObj.data) Array of objects should be returned
        // console.log(largeObj.data[0]) returns the first element in the array so largeObj.data.KEYNAME is usable
                largeObj.data.forEach(subset => {
                //Iterating through the results that best match, not all KEYS have a value, so multiple checks are required
                //Uppercasing all strings to avoid any case sensitive comparisons failing.
                    if(subset.genus && subset.genus.toUpperCase().includes(query) || 
                       subset.common_name && subset.common_name.toUpperCase().includes(query) ||
                       subset.slug && subset.slug.toUpperCase().includes(query) ||
                       subset.family_common_name && subset.family_common_name.toUpperCase().includes(query) ||
                       subset.scientific_name && subset.scientific_name.toUpperCase().includes(query) ||
                       subset.family && subset.family.toUpperCase().includes(query)){
                        plantArray.push(subset);
                    }
                })    
        }
    }
    // console.log(plantArray)
    return plantArray;
}

async function htmlOutput(plantName, image){
    //Creates formatting for a new plant being returned to the user's front end
    //Very lengthy, definitely a candidate for restructuring, its doing too much
    let div = document.createElement('div');
    let innerDiv = document.createElement('div');
    let title = document.createElement('h3');
    let img = document.createElement('img');
    let text = document.createElement('p');
    
    //Button functionality to allow user to add this plant////
    let addToUserButton = document.createElement('button');
    let addToUserform = document.createElement('form');
    let hiddenDataField = document.createElement('input');
    
    addToUserButton.classList += 'btn btn-md btn-success';
    addToUserButton.innerText = 'Add plant to account';
    addToUserButton.type = 'submit';
    addToUserform.method = 'POST';
    addToUserform.action = '/api/plants/add';
    addToUserform.classList += 'form-inline';
    addToUserform.id = 'AddNewPlantAPI';
    hiddenDataField.value = plantName;
    hiddenDataField.type = 'hidden';
    hiddenDataField.name = 'hiddenData';
    
    addToUserform.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formReference = e.target;
        let response = await axios.post(formReference.action, {'hiddenData': hiddenDataField.value})
        alert(response.data.message);
    })

    addToUserform.appendChild(hiddenDataField);
    addToUserform.appendChild(addToUserButton);
    /////////////////////////////////////////////////////////

    // console.log(plantName, query, image) Check to see if data is in!
    div.classList += 'card';
    div.setAttribute('style','display:inline-block !important; width: 20%; margin:auto;');
    innerDiv.classList += 'card-body';
    title.classList += 'card-title';
    text.classList += 'card-text';
    title.innerText = plantName;
    text.innerText = `Here is a picture of a different ${plantName}, Results may vary(feature in beta)`;

    if(image == null || image == undefined){
        //Call flickr API to get a result of images that match name, if none we catch the error and
        //assign a default picture to the result
        try{
            image = await imageAPI(plantName);
            // console.log(image)
            text.innerText = 'Image result may not reflect an accurate representation, feature in beta';

            let farmid = image.photos.photo[0].farm;
            let serverid = image.photos.photo[0].server;
            let secret = image.photos.photo[0].secret;
            let id = image.photos.photo[0].id;

            let flickrURL = `https://farm${farmid}.staticflickr.com/${serverid}/${id}_${secret}.jpg`

            img.src = flickrURL;
            img.classList += 'card-img-bottom img-fluid';
            img.setAttribute('style', 'height:300px; width: 300px;');
        }
        catch(e){
            img.src = '/static/mascot.png';
            img.setAttribute('style', 'height:250px; width:250px;');
            img.classList += 'card-img-bottom img-fluid';
        }
    }
    else{
        img.src = image;
        img.classList += 'card-img-bottom img-fluid';
        img.setAttribute('style', 'height:300px; width: 300px;');
    }

    // console.log(title, img, text); Make sure elements are populated

    div.appendChild(innerDiv);
    innerDiv.appendChild(title);
    innerDiv.appendChild(text);
    innerDiv.appendChild(img);
    innerDiv.appendChild(addToUserform);

    // console.log(div); Final check before submitting

    appendResults.appendChild(div);
    return;
}

async function formatOutput(dataArr, query){
    /*
    *  This function calls the htmlOutput() function with a plant name, and plant image.  
    *  It gets data from the initial API call and then checks it for non null values
    */

    let refinedData;
    let upperQuery = query.toUpperCase(); 
    let errorData = [];

    dataArr.forEach(async plantObj => {
        // console.log(plantObj)
        try{
            if(plantObj.common_name !== null || plantObj.common_name.includes(upperQuery)){
                refinedData = await htmlOutput(plantObj.common_name, plantObj.image_url);
                return refinedData;
            }
            else if(plantObj.family !== null || plantObj.family.includes(upperQuery)){
                refinedData = await htmlOutput(plantObj.family, plantObj.image_url);
                return refinedData;
            }
            else if(plantObj.family_common_name !== null || plantObj.family_common_name.includes(upperQuery)){
                refinedData = await htmlOutput(plantObj.family_common_name, plantObj.image_url);
                return refinedData;
            }
            else if(plantObj.genus !== null || plantObj.genus.includes(upperQuery)){ 
                refinedData = await htmlOutput(plantObj.genus, plantObj.image_url);
                return refinedData;
            }
            else if(plantObj.scientific_name !== null || plantObj.scientific_name.includes(upperQuery)){
                refinedData = await htmlOutput(plantObj.scientific_name, plantObj.image_url);
                return refinedData;
            }
            else if(plantObj.slug !== null || plantObj.slug.includes(upperQuery)){
                refinedData = await htmlOutput(plantObj.slug, plantObj.image_url);
                return refinedData;
            }
            else{
                console.log(`Sorry, something went wrong in sifting data! ${dataArr} ${Object.keys(plantObj)}`);
                return;
            }
        }
        catch(e){
            errorData.push(plantObj)
            
            errorData.forEach(async key => {
                console.log(key.slug)
                if(key.common_name === null){
                    // console.log(`common name ${key.scientific_name}`)
                    return await htmlOutput(key.family, key.image_url);
                }
                else if(key.family === null){
                    return await htmlOutput(key.family_common_name, key.image_url);
                }
                else if(key.family_common_name === null ){
                    return await htmlOutput(key.genus, key.image_url);
                }
                else if(key.genus == null){
                    return await htmlOutput(key.scientific_name, key.image_url);
                }
                else if(key.scientific_name === null){
                    return await htmlOutput(key.slug, key.image_url);
                }
                else if(key.common_name === null){
                    return await htmlOutput(key.slug, key.image_url)
                }
                else{
                    console.log(`${e}; Failed Search`)
                    return;
                }
            })
        }
    })
}

let searchPlant = document.querySelector('#searchPlant');
let appendResults = document.querySelector('#plant-search-output');

searchPlant.addEventListener('submit', async (e) => {
    e.preventDefault();

    while (appendResults.firstChild) {
        appendResults.removeChild(appendResults.firstChild);
    }

    let query = document.querySelector('#searchQuery').value;
    let newSearch = new SearchPlantAPI();
    let dataOfSearch = await newSearch.GetPlant(query);
    let siftedData = filterData(dataOfSearch, query);
    await formatOutput(siftedData, query);
})