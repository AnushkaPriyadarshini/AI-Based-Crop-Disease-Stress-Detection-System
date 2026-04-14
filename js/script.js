
const cropDiseases = {
    'Tomato': [
        { name: 'Leaf Mold', 
        desc: 'Caused by the fungus *Passalora fulva*, leading to yellow spots and fuzzy mold on the undersides of leaves.' ,
        img : 'static/images/leaf_mold_tomato.jpg'},
        { name: 'Tomato Mosaic Virus', 
        desc: 'Viral disease causing mottled, curled leaves and reduced fruit quality.',
        img : 'static/images/tomato_mosaic_virus.jpg' },
        { name: 'Septoria Leaf Spot', 
        desc: 'Fungal infection causing small, dark spots with gray centers on leaves, leading to defoliation.',
        img : 'static/images/tomato_septoria_leaf_spot.jpg' },
        { name: 'Early Blight', 
        desc: 'Caused by *Alternaria solani*, leading to brown, concentric rings on older leaves.' ,
        img : 'static/images/tomato_early_blight.jpg'},
        { name: 'Tomato Yellow Leaf Curl Virus', 
        desc: 'Transmitted by whiteflies, causing curled, yellow leaves and stunted plant growth.' ,
        img : 'static/images/tomato_yellow_leaf_curl_virus.jpg'},
        { name: 'Bacterial Spot',
        desc: 'Bacterial infection causing small, water-soaked spots on leaves and fruit.',
        img: 'static/images/tomato_bacterial_spot.jpg'},
    ],

    'Apple': [
        { name: 'Apple Scab', 
        desc: 'Fungal disease causing olive-green spots on leaves and fruit, reducing quality.' ,
        img: 'static/images/apple-scab.jpg'},

        { name: 'Cedar Apple Rust', 
        desc: 'Fungal disease requiring juniper hosts, causing orange leaf spots and fruit damage.' , 
        img:'static/images/cedar-apple.jpg' },

        { name: 'Black Rot', 
        desc: 'Caused by *Botryosphaeria obtusa*, leading to black, shriveled fruit and leaf lesions.' , 
        img: 'static/images/apple-black_rot.jpg'}
    ],

    'Grape': [
        { name: 'Black Rot', 
        desc: 'Fungal infection causing brown leaf lesions and shriveled black fruit.',
        img: 'static/images/grape_black_rot.jpg' },

        { name: 'Leaf Blight (Isariopsis Leaf Spot)', 
        desc: 'Spreads rapidly in humid conditions, causing brown necrotic lesions on leaves.',
        img: 'static/images/grape_leaf_blight.jpg' },

        { name: 'Esca (Black Measles)', 
        desc: 'Complex disease leading to striped discoloration on leaves and internal wood decay.' ,
        img: 'static/images/grape_black_measles.jpg'}
    ],

    'Corn_(maize)': [
        { name: 'Northern Leaf Blight', 
        desc: 'Caused by *Exserohilum turcicum*, forming long, gray-green leaf lesions.',
        img:'static/images/corn_northern_leaf_blight.jpg' },

        { name: 'Common Rust', 
        desc: 'Fungal disease creating reddish-brown pustules on leaves, reducing photosynthesis.' , 
        img:'static/images/corn_common_rust.jpg' },

        { name: 'Cercospora Leaf Spot (Gray Leaf Spot)', 
        desc: 'Leads to rectangular, grayish-brown lesions, reducing crop yield.',
        img: 'static/images/corn_spot_grey.jpg'}
    ],

    'Orange': [
        { name: 'Huanglongbing (Citrus Greening)', 
        desc: 'Bacterial disease spread by psyllid insects, causing yellow shoots, bitter fruit, and tree decline.',
        img: 'static/images/orange_citrus_greening.jpg' }
    ],

    'Peach': [
        { name: 'Bacterial Spot', 
        desc: 'Caused by *Xanthomonas arboricola*, leading to small, dark lesions on leaves and fruit.' , 
        img: 'static/images/peach_bacterial_spot.jpg' }
    ],

    'Pepper,bell': [
        { name: 'Bacterial Spot',
         desc: 'Bacterial infection causing small, water-soaked spots on leaves that turn brown and crack.',
         img: 'static/images/bell_pepper_bacterial_spot.jpg' }
    ],

    'Potato': [
        { name: 'Early Blight', 
        desc: 'Caused by *Alternaria solani*, forming dark, concentric rings on older leaves, reducing yield.',
        img: 'static/images/potato_early_blight.jpg' },

        { name: 'Late Blight', 
        desc: 'Serious fungal disease leading to dark, water-soaked lesions that rapidly spread in wet conditions.' , 
        img:'static/images/potato_late_blight.jpg' }
    ]
};



function updateDiseases() {
    const crop = document.getElementById("cropDropdown").value;
    const diseaseList = document.getElementById("disease-list");
    diseaseList.innerHTML = "";  

    if (cropDiseases[crop]) {
const ul = document.createElement("ul");
cropDiseases[crop].forEach(disease => {
    const li = document.createElement("li");
    li.innerHTML = `<strong>${disease.name}:</strong> ${disease.desc}`;
    if (disease.img) {
        li.innerHTML += `<br><img src="${disease.img}" alt="${disease.name}" width="150">`; // Display image
    }
    ul.appendChild(li);
});
        diseaseList.appendChild(ul);
    } else {
        diseaseList.innerHTML = "<p>No disease data available.</p>";
    }
}

document.getElementById("cropDropdown").addEventListener("change", updateDiseases);

window.onload = function () {
    let fileInput = document.getElementById("imageInput");

    fileInput.addEventListener("change", function () {
        if (!fileInput.files.length) {
            document.getElementById("crop-mapping").innerText = "Name of the detected crop is : ";
            document.getElementById("disease-name").innerText = "Disease detected is : ";
           // document.getElementById("temperature").innerText = "Temperature of your location is : ";
           // document.getElementById("humdity").innerText = "Humidity of your location is : ";
            document.getElementById("disease-severity").innerText = "Environmental Severity Risk : ";
            document.getElementById("genetic suggestion").innerHTML = "<u>Genetic Suggestions : </u><br><br>";
        }
    });
};

