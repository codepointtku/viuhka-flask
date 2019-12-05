$('#dateTimePicker').on('click', function (event) {
    event.preventDefault();
    $('timePicker').show();
});
$('#selectCategoryForm').on('submit', function (event) {
    event.preventDefault();
    $(this).serializeArray().forEach(function (i, k) {
        if ($('#' + i.value.split(' ').join('')).length == 0) {
            $('#category_items').append(
                '<option id=' + i.value.split(' ').join('') + ' selected>' + i.value + '</option>'
            );
        }
    });
    setTimeout(function () {
        $('#selectCategories').modal('hide');
    }, 125);
});
$('#deleteCategoryItem').on('click', function (event) {
    event.preventDefault();
    $('#category_items option:selected').remove();
});

// these dont appear to be in use??