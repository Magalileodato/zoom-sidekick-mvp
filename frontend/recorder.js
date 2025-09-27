/**
 * recorder.js - Captura áudio e interage com o backend
 * -----------------------------------------------------
 * Funcionalidades:
 * 1. Captura do microfone usando MediaRecorder API.
 * 2. Envio do áudio para o backend via fetch POST.
 * 3. Atualiza transcrição, resumo e toca áudio da próxima pergunta.
 */

let mediaRecorder;
let audioChunks = [];

// Seleciona elementos do DOM
const recordButton = document.getElementById("record-btn");
const transcriptionDiv = document.getElementById("transcription");
const summaryDiv = document.getElementById("summary");
const audioPlayer = document.getElementById("next-question-audio");
const questionDiv = document.getElementById("question");

async function initMicrophone() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            // Converte chunks em blob de áudio
            const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
            audioChunks = []; // Limpa para próxima gravação

            // Envia áudio para o backend
            await sendAudio(audioBlob);
        };
    } catch (error) {
        console.error("Erro ao acessar microfone:", error);
        alert("Não foi possível acessar o microfone. Verifique permissões.");
    }
}

async function sendAudio(audioBlob) {
    const formData = new FormData();
    formData.append("audio", audioBlob, "response.webm");

    try {
        const response = await fetch("/answer", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Erro ao enviar áudio: ${response.statusText}`);
        }

        const data = await response.json();

        // Atualiza transcrição e resumo
        transcriptionDiv.textContent = data.transcription || "Sem transcrição";
        summaryDiv.textContent = data.summary || "Sem resumo";

        // Atualiza e toca próxima pergunta em áudio
        if (data.next_question_audio) {
            audioPlayer.src = `/play_audio/${data.next_question_audio.split('/').pop()}`;
            audioPlayer.play();
        }

    } catch (error) {
        console.error("Erro ao processar áudio:", error);
        alert("Ocorreu um erro ao processar a resposta.");
    }
}

// Botão de gravação
recordButton.addEventListener("click", () => {
    if (!mediaRecorder) {
        alert("Microfone não inicializado");
        return;
    }

    if (mediaRecorder.state === "inactive") {
        mediaRecorder.start();
        recordButton.textContent = "Parar Gravação";
    } else if (mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        recordButton.textContent = "Iniciar Gravação";
    }
});

// Inicializa o microfone ao carregar a página
window.addEventListener("DOMContentLoaded", initMicrophone);
