// =============================================================================
// FRONTEND — Analizador Léxico: AJAX, eventos, interactividad
// =============================================================================

document.addEventListener("DOMContentLoaded", function () {
  const editor = document.getElementById("editor");
  const btnAnalizar = document.getElementById("btn-analizar");
  const btnEjemplo = document.getElementById("btn-ejemplo");
  const btnLimpiar = document.getElementById("btn-limpiar");
  const fileInput = document.getElementById("file-input");
  const resultadoColoreado = document.getElementById("resultado-coloreado");
  const statusMsg = document.getElementById("status-msg");
  const statTotal = document.getElementById("stat-total");
  const statValido = document.getElementById("stat-valido");
  const statInv = document.getElementById("stat-inv");
  const statsBar = document.getElementById("stats-bar");
  const statsGrid = document.getElementById("stats-grid");
  const seccionStats = document.getElementById("seccion-stats");
  const tablaTokens = document.getElementById("tabla-tokens");
  const seccionTabla = document.getElementById("seccion-tabla");
  const filtroTabla = document.getElementById("filtro-tabla");

  // -----------------------------------------------------------------------
  // Ejemplo de código para análisis
  // -----------------------------------------------------------------------

  const CODIGO_EJEMPLO = `// Ejemplo: función para calcular factorial
entero factorial(entero n) {
  si (n <= 1) {
    retornar 1;
  } sino {
    retornar n * factorial(n - 1);
  }
}

// Variables de prueba
entero num = 5;
decimal pi = 3.1416;
booleano activo = verdadero;

// Expresión lógica
si (num > 0 && activo || num != 10) {
  // Operaciones aritméticas
  decimal resultado = num + pi * 2;
  mientras (resultado >= 10) {
    resultado = resultado / 2;
  }
}
`;

  // -----------------------------------------------------------------------
  // Evento: Botón "Ejemplo"
  // -----------------------------------------------------------------------

  btnEjemplo.addEventListener("click", function () {
    editor.value = CODIGO_EJEMPLO;
    showStatus("Ejemplo cargado", "status-ok");
  });

  // -----------------------------------------------------------------------
  // Evento: Botón "Limpiar"
  // -----------------------------------------------------------------------

  btnLimpiar.addEventListener("click", function () {
    editor.value = "";
    resultadoColoreado.innerHTML = `<p class='placeholder-text'>El resultado aparecerá aquí...</p>`;
    statsBar.classList.add("hidden");
    seccionStats.classList.add("hidden");
    seccionTabla.classList.add("hidden");
    showStatus("Limpiado", "status-ok");
  });

  // -----------------------------------------------------------------------
  // Evento: Botón "Analizar"
  // -----------------------------------------------------------------------

  btnAnalizar.addEventListener("click", function () {
    const codigo = editor.value;

    if (!codigo.trim()) {
      showStatus("Por favor, escribe código para analizar", "status-error");
      return;
    }

    realizarAnalisis(codigo);
  });

  // -----------------------------------------------------------------------
  // Evento: Upload de archivo
  // -----------------------------------------------------------------------

  fileInput.addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.name.endsWith(".txt")) {
      showStatus("Solo se aceptan archivos .txt", "status-error");
      fileInput.value = "";
      return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
      const codigo = e.target.result;
      editor.value = codigo;
      realizarAnalisis(codigo);
      fileInput.value = "";
    };
    reader.onerror = function () {
      showStatus("Error al leer el archivo", "status-error");
      fileInput.value = "";
    };
    reader.readAsText(file);
  });

  // -----------------------------------------------------------------------
  // Filtro de tabla
  // -----------------------------------------------------------------------

  filtroTabla.addEventListener("input", function () {
    const query = filtroTabla.value.toLowerCase();
    const filas = document.querySelectorAll(".token-table tbody tr");

    filas.forEach((fila) => {
      const lexema = fila.cells[1].textContent.toLowerCase();
      const tipo = fila.cells[2].textContent.toLowerCase();

      if (lexema.includes(query) || tipo.includes(query)) {
        fila.style.display = "";
      } else {
        fila.style.display = "none";
      }
    });
  });

  // -----------------------------------------------------------------------
  // Función principal: análisis AJAX
  // -----------------------------------------------------------------------

  function realizarAnalisis(codigo) {
    showStatus("Analizando...", "status-msg");
    btnAnalizar.disabled = true;

    fetch("/analizar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ codigo: codigo }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Error en la respuesta del servidor");
        }
        return response.json();
      })
      .then((data) => {
        // Mostrar resultado coloreado
        resultadoColoreado.innerHTML = data.html_coloreado;

        // Mostrar tabla
        if (data.tabla_html) {
          tablaTokens.innerHTML = data.tabla_html;
          seccionTabla.classList.remove("hidden");
          filtroTabla.value = "";
        }

        // Mostrar estadísticas
        if (data.estadisticas) {
          const stats = data.estadisticas;

          statTotal.textContent = `${stats.total} tokens`;
          statValido.textContent = `${stats.validos} válidos`;
          statInv.textContent = `${stats.invalidos} inválidos`;
          statsBar.classList.remove("hidden");

          // Grid de estadísticas por tipo
          statsGrid.innerHTML = "";
          for (const [tipo, cantidad] of Object.entries(stats.por_tipo)) {
            const card = document.createElement("div");
            card.className = "stat-card";
            card.innerHTML = `
              <div class="stat-card-label">${tipo}</div>
              <div class="stat-card-value" style="color: ${stats.colores[tipo] || '#e2e8f0'}">
                ${cantidad}
              </div>
            `;
            statsGrid.appendChild(card);
          }
          seccionStats.classList.remove("hidden");
        }

        showStatus(`✓ Análisis completado: ${data.tokens.length} tokens`, "status-ok");
      })
      .catch((error) => {
        showStatus(`✗ Error: ${error.message}`, "status-error");
        resultadoColoreado.innerHTML = `<p class='placeholder-text' style='color: var(--c-invalido)'>Error al procesar.</p>`;
      })
      .finally(() => {
        btnAnalizar.disabled = false;
      });
  }

  // -----------------------------------------------------------------------
  // Utilidad: mostrar mensaje de estado
  // -----------------------------------------------------------------------

  function showStatus(message, className) {
    statusMsg.textContent = message;
    statusMsg.className = `status-msg ${className}`;
    setTimeout(() => {
      statusMsg.textContent = "";
      statusMsg.className = "status-msg";
    }, 4000);
  }
});
