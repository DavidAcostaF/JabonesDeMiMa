let loadingSpinner = document.querySelector('#overlay-spinner')
loadingSpinner.style.visibility = 'hidden';

function toggleLoadingScreen(visible) {
    console.log(`[DEBUG] toggleLoadingScreen: ${visible}`);
    let loadingSpinner = document.querySelector('#overlay-spinner');
    loadingSpinner.style.visibility = visible ? 'visible' : 'hidden';
}

const generate_report = async (url, filename, btn_id = "download_button") => {
    console.log("[DEBUG] Generating report...");
    let button = document.getElementById(btn_id);
    button.disabled = true;
    toggleLoadingScreen(true);

    let filtros = document.getElementById("filters");
    let formData = new FormData(filtros);
    let queryString = new URLSearchParams(formData).toString();
    console.log("[DEBUG] Query string:", queryString);

    const fullUrl = url + `?${queryString}`;
    console.log("[DEBUG] Fetching URL:", fullUrl);

    const response = await fetch(fullUrl);

    if (!response.ok) {
        console.error("[ERROR] Response not OK:", response.status);
        button.disabled = false;
        toggleLoadingScreen(false);
        Swal.fire({
            title: '¡Error!',
            text: "No se pudo generar el reporte",
            icon: 'error',
            confirmButtonText: 'Continuar',
            customClass: {
                confirmButton: 'btn btn_confirm_modal btn_guardar',
                cancelButton: 'btn btn_cancel_modal btn_rounded'
            },
        });
        return;
    }

    const responseJSON = await response.json();
    console.log("[DEBUG] Response JSON:", responseJSON);

    switch (responseJSON.type) {
        case 'xlsx':
            console.log("[DEBUG] Generating Excel file...");
            generate_excel(responseJSON.data, filename, button);
            toggleLoadingScreen(false);
            break;
        case 'json':
            console.log("[DEBUG] Generating CSV...");
            generate_csv(responseJSON.data, button);
            toggleLoadingScreen(false);
            break;
        default:
            console.error("[ERROR] Tipo de archivo no reconocido:", responseJSON.type);
            button.disabled = false;
            toggleLoadingScreen(false);
            Swal.fire({
                title: '¡Error!',
                text: "No se pudo generar el reporte",
                icon: 'error',
                confirmButtonText: 'Continuar',
                customClass: {
                    confirmButton: 'btn btn_confirm_modal btn_guardar',
                    cancelButton: 'btn btn_cancel_modal btn_rounded'
                },
            });
            return;
    }
};

const generate_excel = async (data, filename, button) => {
    console.log("[DEBUG] Generating Excel from base64...");
    let mediaType = "data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,";
    let uri = mediaType + data;
    let a = document.createElement("a");
    a.href = uri;
    a.download = filename;
    a.click();
    button.disabled = false;
};

const generate_csv = async (data, button) => {
    console.log("[DEBUG] Initializing ConversorJSON for CSV...");
    new ConversorJSON(data, button);
};

class ConversorJSON {

    CHUNK_SIZE = 256;
    WRITE_INTERVAL = 10;
    buttonElement = undefined;
    divProgressElement = undefined;

    convertedPages = 0;
    totalPages = 0;

    constructor(data, buttonElement) {
        console.log("[DEBUG] ConversorJSON constructor");
        this.buttonElement = buttonElement;

        this.divProgressElement = document.createElement('div');
        this.divProgressElement.style.display = 'grid';
        this.divProgressElement.id = crypto.randomUUID();
        this.buttonElement.appendChild(this.divProgressElement);

        this.handleFile(data);
    }

    handleFile(data) {
        console.log("[DEBUG] Decoding base64 data...");
        let jsonData = atob(data);
        console.log("[DEBUG] Base64 decoded data (preview):", jsonData.slice(0, 100));

        try {
            jsonData = JSON.parse(jsonData);
            console.log("[DEBUG] Parsed JSON:", jsonData);
        } catch (error) {
            console.error('❌ Error en lectura de JSON', error);
            alert("Hubo un error, revisar información.");
            return;
        }

        if (!Array.isArray(jsonData)) {
            console.error('❌ El objeto no es un array:', jsonData);
            alert("Hubo un error, revisar información.");
            return;
        }

        if (jsonData.length <= 0) {
            console.warn("⚠️ El JSON está vacío");
            alert("No hay datos para generar el reporte.");
            return;
        }

        this.convertedPages = 0;
        this.totalPages = jsonData.length;

        jsonData.forEach(item => {
            console.log("[DEBUG] Procesando item:", item);
            this.processDataInChunks(item);
        });
    }

    arrayToCSV(columns) {
        return columns.map(col => `"${col}"`).join(",") + "\n";
    }

    async processDataInChunks(item) {
        console.log("[DEBUG] Procesando chunks para:", item.ws_name);
        let csvContent = this.arrayToCSV(item.columns);
        let processed = 0;

        const progressBar = document.createElement('progress');
        progressBar.id = crypto.randomUUID();
        progressBar.max = item.data.length;
        this.divProgressElement.appendChild(progressBar);

        for (let i = 0; i < item.data.length; i += this.CHUNK_SIZE) {
            const chunk = item.data.slice(i, i + this.CHUNK_SIZE);
            console.log(`[DEBUG] Chunk ${i / this.CHUNK_SIZE + 1}:`, chunk);
            chunk.forEach(row => csvContent += row.map(value => `"${value}"`).join(",") + "\n");
            await new Promise(resolve => setTimeout(resolve, this.WRITE_INTERVAL));
            processed += chunk.length;
            progressBar.value = processed;
        }

        progressBar.remove();
        this.downloadCSV(item.ws_name, csvContent);
        this.convertedPages += 1;

        if (this.convertedPages >= this.totalPages) {
            this.buttonElement.disabled = false;
            this.divProgressElement.remove();
        }
    }

    downloadCSV(filename, csvContent) {
        console.log("[DEBUG] Descargando CSV:", filename);
        const encodedContent = new TextEncoder().encode(csvContent, { encoding: 'utf-8' });
        const utf8Bom = "\uFEFF";
        const blob = new Blob([utf8Bom, encodedContent], { type: 'text/csv;charset=utf-8' });
        const link = document.createElement("a");
        const url = URL.createObjectURL(blob);
        link.setAttribute("href", url);
        link.setAttribute("download", filename + ".csv");
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}
