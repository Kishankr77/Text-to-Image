const generateBtn = document.getElementById("generateBtn");
const outputImg = document.getElementById("output");
const loader = document.getElementById("loader");
const promptInput = document.getElementById("prompt");
const placeholderText = document.getElementById("placeholderText");


const styleSelect = document.getElementById("style-select");
const ratioSelect = document.getElementById("ratio-select");
const downloadBtn = document.getElementById("downloadBtn"); 


outputImg.style.display = "none";
loader.style.display = "none";
placeholderText.style.display = "block"; 
downloadBtn.style.display = "none"; 


function setUiState(isGenerating) {
    if (isGenerating) {
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...'; 
        loader.style.display = "block";
        outputImg.style.display = "none";
        placeholderText.style.display = "none"; 
        downloadBtn.style.display = "none"; 
    } else {
        
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-wand-magic-sparkles"></i> Generate'; 
        loader.style.display = "none";
    }
}


generateBtn.addEventListener("click", async () => {
    const userPrompt = promptInput.value.trim();
    const selectedStyle = styleSelect.value;
    const aspectRatio = ratioSelect.value;

    if (!userPrompt) {
        alert("Please enter a prompt to generate an image!");
        return;
    }

    
    let finalPrompt = userPrompt;
    if (selectedStyle) {
        finalPrompt = `${userPrompt}, ${selectedStyle}`;
    }

    setUiState(true);

    try {
        const response = await fetch("http://127.0.0.1:5000/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                prompt: finalPrompt,
                ratio: aspectRatio
            })
        });

        const data = await response.json();

        if (response.ok && data.image) {
            
            const imageUri = "data:image/png;base64," + data.image;
            outputImg.src = imageUri;
            outputImg.style.display = "block";
            placeholderText.style.display = "none";
            
            
            downloadBtn.href = imageUri; 
            downloadBtn.style.display = "inline-block"; 

        } else {
            const errorMessage = data.error || "Unknown server error occurred.";
            alert("Error: " + errorMessage);
            placeholderText.style.display = "block"; 
            downloadBtn.style.display = "none"; 
        }

    } catch (err) {
        // Network error
        console.error("Fetch Error:", err);
        alert("Failed to connect to the backend server. Make sure 'app.py' is running on http://127.0.0.1:5000.");
        placeholderText.style.display = "block";
        downloadBtn.style.display = "none"; 
    } finally {
        setUiState(false);
    }
});