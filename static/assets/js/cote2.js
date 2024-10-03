$.ajax({
  type: "get",
  url: "/examens-repechages/fetch",
  dataType: "json",
  success: function (data) {
    $("#classe_id").change(function (e) {
      const classe_id = e.target.value;
      const cours = data.cours.filter((cours) =>
        data.sessions.some((session) => session.cours_id == cours.id)
      );
      $("#cours").empty();
      $("#cours").append("<option>Sélectionnez un cours</option>");
      cours.forEach((cours) => {
        $("#cours").append(
          `<option value='${cours.id}'>${cours.designation}</option>`
        );
      });

      $("#cours").change((e) => {
        const cours_id = e.target.value;
        const coterBtn = $("#coter");
        coterBtn.removeAttr("disabled");
        coterBtn.click(function (e) {
          const fiche = $("#fiche");
          e.preventDefault();
          $("#span_cours").html(
            data.cours.find((cours) => cours.id == cours_id).designation
          );
          fiche.empty();
          const eleveSessions = data.sessions
            .filter((session) => session.cours_id == cours_id)
            .map((session) => ({
              ...session,
              eleve: data.eleves.find((eleve) => eleve.id == session.eleve_id),
            }));

          eleveSessions.forEach((session) => {
            fiche.append(`
              <div class="row justofy-content-center align-items-center">
              <div class="col-5">
                <span>${session.eleve.nom} ${session.eleve.postnom} ${
              session.eleve.prenom ?? ""
            }</span>
              </div>
              <div class="col-7">
                <div class="input-group mb-3">
                  <input
                    type="number"
                    class="form-control"
                    placeholder="cote"
                    aria-label="cote"
                    min="0"
                    value="0"
                    max="100"
                    name="pourcentage_${session.id}"
                    aria-describedby="basic-addon1"
                  />
                  <span class="input-group-text" id="basic-addon1"
                    >/100</span
                  >
                </div>
              </div>
            </div>
              `);
          });
          $("#fiche input.form-control").on("input", (e) => {
            if (parseInt(e.target.value) > ponderation) {
              $(this).val(ponderation);
            }
          });
        });
      });
    });
  },
});
