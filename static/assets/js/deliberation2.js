$.ajax({
  type: "get",
  url: "/examens-repechages/fetch",
  dataType: "json",
  success: function (data) {
    const sessions = data.repechages;
    const inscrits = data.inscrits.filter((inscrit) =>
      sessions.some((session) => session.eleve_id == inscrit.eleve_id)
    );
    const critere = $("#critere");
    critere.change((e) => {
      const eleves = inscrits
        .map((inscrit) => {
          const eleve = data.eleves.find(
            (eleve) => eleve.id == inscrit.eleve_id
          );
          const classe = data.classes.find(
            (classe) => (classe.id = inscrit.classe_id)
          );
          const sessionsEleve = sessions.filter(
            (session) => session.eleve_id == inscrit.eleve_id
          );
          return {
            noms: `${eleve.nom} ${eleve.postnom} ${eleve.prenom ?? ""}`,
            classe_id: classe.id,
            classe: `${classe.designation} ${
              data.options.find((option) => option.id == classe.option_id)
                .designation
            }`,
            nbSessions: sessionsEleve.length,
            SV: sessionsEleve.filter((session) => session.pourcentage >= 50)
              .length,
            SNV: sessionsEleve.filter((session) => session.pourcentage < 50)
              .length,
          };
        })
        .sort((a, b) => a.classe.localeCompare(b.classe));
      const eleveCritiere = eleves.filter(
        (eleve) => (eleve.SV / eleve.SNV) * 100 >= parseFloat(e.target.value)
      );
      $("#data").empty();
      eleveCritiere.forEach((eleve, index) => {
        $("#data").append(
          `<div class="col">
              <input type="number" id="num" value="${
                index + 1
              }" class="form-control" readonly>
            </div>
            <div class="col-3">
              <input type="text" id="noms" value="${
                eleve.noms
              }" class="form-control" readonly>
            </div>
            <div class="col text-center">
              <input type="text" id="classe" value="${
                eleve.classe
              }" class="form-control" readonly>
            </div>
            <div class="col text-center">
              <input type="number" id="NbS" value="${
                eleve.nbSessions
              }" class="form-control" readonly>
            </div>
            <div class="col text-center">
              <input type="number" id="SV" value="${
                eleve.SV
              }" class="form-control" readonly>
            </div>
            <div class="col text-center">
              <input type="number" id="SNV" value="${
                eleve.SNV
              }" class="form-control" readonly>
            </div>`
        );
      });
    });
  },
});
