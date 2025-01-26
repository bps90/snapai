function calculateDegree() {
    $.ajax({
        url: "calculate_degree/?node_id=" + $("#degree-algorithm-node").val(),
        type: "GET",
        success: function (data) {

            $("#degree-result").val(data.degree);
        },
        error: function (xhr, status, error) {
            console.error(error, xhr?.responseJSON?.message);
            $("#degree-result").attr("title", xhr?.responseJSON?.message || "Erro ao calcular grau");
            $("#degree-result").val(xhr?.responseJSON?.message || "Erro ao calcular grau");
        },
    })
}

function calculateDiameter() {
    $.ajax({
        url: "calculate_diameter/",
        type: "GET",
        success: function (data) {

            $("#diameter-result").val(data.diameter);
        },
        error: function (xhr, status, error) {
            console.error(error, xhr?.responseJSON?.message);
            $("#diameter-result").attr("title", xhr?.responseJSON?.message || "Erro ao calcular diametro");
            $("#diameter-result").val(xhr?.responseJSON?.message || "Erro ao calcular diametro");
        },
    });
}

function calculateEccentricity() {
    const nodeId = $("#eccentricity-algorithm-node").val();

    $.ajax({
        url: "calculate_eccentricity/?node_id=" + nodeId,
        type: "GET",
        success: function (data) {
            $("#eccentricity-result").val(data.eccentricity);
        },
        error: function (xhr, status, error) {
            console.error(error, xhr?.responseJSON?.message);
            $("#eccentricity-result").attr("title", xhr?.responseJSON?.message || "Erro ao calcular excentricidade");
            $("#eccentricity-result").val(xhr?.responseJSON?.message || "Erro ao calcular excentricidade");
        },
    });
}