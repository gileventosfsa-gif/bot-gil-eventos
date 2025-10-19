// static/script.js

document.addEventListener("DOMContentLoaded", function() {
    console.log("🎉 Gil Eventos - Script carregado");

    // Exemplo: aumentar/diminuir quantidade nos pedidos
    document.querySelectorAll(".btn-increment").forEach(btn => {
        btn.addEventListener("click", function() {
            let input = this.closest(".pedido-item").querySelector(".qtd");
            input.value = parseInt(input.value) + 1;
        });
    });

    document.querySelectorAll(".btn-decrement").forEach(btn => {
        btn.addEventListener("click", function() {
            let input = this.closest(".pedido-item").querySelector(".qtd");
            let current = parseInt(input.value);
            if (current > 1) input.value = current - 1;
        });
    });

    // Exemplo: enviar pedido via formulário
    const form = document.getElementById("pedido-form");
    if (form) {
        form.addEventListener("submit", function(e) {
            e.preventDefault();
            const data = new FormData(form);
            fetch("/novo-pedido", {
                method: "POST",
                body: data
            })
            .then(res => res.json())
            .then(resp => {
                alert(resp.message);
                if(resp.success) {
                    form.reset();
                }
            })
            .catch(err => {
                console.error("Erro ao enviar pedido:", err);
                alert("Erro ao enviar pedido, tente novamente.");
            });
        });
    }
});
