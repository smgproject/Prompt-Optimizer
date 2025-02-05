document.getElementById("optimize-btn").addEventListener("click", optimizePrompt);

async function optimizePrompt() {
    const prompt = document.getElementById("prompt-input").value.trim();
    const tone = document.getElementById("tone-selector").value;
    
    if (!prompt) {
        alert("Please enter a prompt.");
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/optimize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt, tone })
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to optimize prompt');
        }

        displayGeneratedPrompts([data.optimized_prompt]);
    } catch (error) {
        console.error('Error:', error);
        alert(`Error: ${error.message}`);
    }
}

function displayGeneratedPrompts(prompts) {
    const samplesContainer = document.getElementById("samples");
    samplesContainer.innerHTML = prompts.map(p => 
        `<div class="prompt-card">
            <p>${p}</p>
            <button class="copy-btn">Copy</button>
        </div>`
    ).join('');

    // Add copy functionality
    document.querySelectorAll('.copy-btn').forEach((btn, index) => {
        btn.addEventListener('click', () => {
            navigator.clipboard.writeText(prompts[index]);
            btn.textContent = 'Copied!';
            setTimeout(() => btn.textContent = 'Copy', 2000);
        });
    });
}