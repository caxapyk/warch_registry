function removeSelected() {
  if (confirm('Вы уверены что хотите удалить выбранные элементы?')) {
    var form = document.getElementById("selected-form");
    form.submit();
  }
}

$(document).ready(function () {
  $('#selected-remove').click(function () {
    removeSelected();
  });

  $('.add-related-popup').click(function (e) {
    openPopup(this);
    e.preventDefault();
  });

  feather.replace()
});