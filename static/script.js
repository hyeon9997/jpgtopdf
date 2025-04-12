document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const fileInput = document.getElementById("pdfFile");

    form.addEventListener("submit", function (e) {
        if (!fileInput.files.length) {
            e.preventDefault();
            alert("PDF 파일을 선택해주세요.");
            return;
        }

        const button = form.querySelector("button");
        button.disabled = true;
        button.textContent = "변환 중... 잠시만 기다려주세요.";
    });
});
