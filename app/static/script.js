document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("expense-form");
  const list = document.getElementById("expenses");

  let editId = null;

  function loadExpenses() {
    fetch("/expenses")
      .then((res) => res.json())
      .then((data) => {
        list.innerHTML = "";
        data.forEach((e) => {
          const li = document.createElement("li");
          li.innerHTML = `
            ${e.category} - ₹${e.amount} on ${e.date}
            <button onclick="editExpense(${e.id}, '${e.amount}', '${e.category}', '${e.date}')">✏️</button>
            <button onclick="deleteExpense(${e.id})">🗑️</button>
          `;
          list.appendChild(li);
        });
      });
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const amount = parseFloat(document.getElementById("amount").value);
    const category = document.getElementById("category").value;
    const date = document.getElementById("date").value;

    const payload = { amount, category, date };

    if (editId) {
      // PUT request
      fetch(`/expenses/${editId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      }).then(() => {
        editId = null;
        form.reset();
        loadExpenses();
      });
    } else {
      // POST request
      fetch("/expenses", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      }).then(() => {
        form.reset();
        loadExpenses();
      });
    }
  });

  // Expose functions globally
  window.deleteExpense = (id) => {
    fetch(`/expenses/${id}`, {
      method: "DELETE"
    }).then(() => loadExpenses());
  };

  window.editExpense = (id, amount, category, date) => {
    document.getElementById("amount").value = amount;
    document.getElementById("category").value = category;
    document.getElementById("date").value = date;
    editId = id;
  };

  loadExpenses();
});
