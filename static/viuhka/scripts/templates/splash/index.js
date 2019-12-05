$(document).ready(function () {
    var spinner = $('#searchSpinner');
    var rows = $('#serviceTable tr');
    var results = $('#results');
    var paginationNum;
    var totalResults;
    var visibleResults;
    $(spinner).hide();
    updateResults();

    function updateResults() {
        results.text($('td:visible').length + ' results of ' + total);
        visibleResults = $('td:visible');
        totalResults = $('td.result');
        paginationNum = visibleResults.length / 25;
       $(visibleResults[0]).addClass('first-result');
//       console.log('pagination amount ' + Math.round(paginationNum));
//       console.log(totalResults.length);

    }

    function addResult(x) {
        if(!$(x).hasClass('result')){
            $(x).addClass('result');
        }
    }

    function removeResult(x) {
        if($(x).hasClass('result')){$(x).removeClass('result')}
    }

    $('#serviceSearch').on('keyup', function () {
        $(spinner).show();

        var search = $(this).val().toUpperCase();
        for (i = 0; i < rows.length; i++) {
            td = rows[i].getElementsByTagName('td')[0];

            title = td.getElementsByTagName('h2')[0];
            organization = td.getElementsByTagName('p')[0];
            ingress = td.getElementsByTagName('p')[1];

            if (~title.innerText.toUpperCase().indexOf(search) || ~organization.innerText.toUpperCase().indexOf(search) || ~ingress.innerText.toUpperCase().indexOf(search)) {
                addResult(td);

                $(td).show(25);
            } else {
                removeResult(td);

                $(td).hide();
            }
        }
        rows = $('#serviceTable tr');
        $('a[id=resetFilters').text('Poista hakusuodattimet');
        $('a[id=resetFilters').show();
        setTimeout(function () {
            $(spinner).hide();
        }, 375);
        updateResults();
    });

    $('a[id^=cg_').on('click', function () {
        if (!$(this).attr('aria-expanded') || $(this).attr('aria-expanded') === 'false') {
            $(spinner).show();
            var found = []
            var categoryItems = $('a[cgItemCategoryId^=' + $(this).attr('categoryId') + ']');
            $(categoryItems).each(function (idx, val) {
                for (i = 0; i < rows.length; i++) {
                    td = rows[i].getElementsByTagName('td')[0];
                    if (td) {
                        if ($(td).hasClass($(val).attr('sanitized'))) {
                            found.push($(td));
                        }
                        $(td).hide();
                        removeResult(td);
                    }
                }
            });
            found.forEach(function (idx, val) {
                addResult(found[val]);
                $(found[val]).show(11);
            
            });
            setTimeout(function () {
                $(spinner).hide();
            }, 375);
            $('a[id=resetFilters').text('Poista hakusuodattimet');
            $('a[id=resetFilters').show();
        } else {
            $('a[id=resetFilters]').click();
        }
        updateResults();
    });
    $('a[id^=cgItem_]').on('click', function () {
        var found = []
        $(this).each(function (idx, val) {
            for (i = 0; i < rows.length; i++) {
                td = rows[i].getElementsByTagName('td')[0];
                if (td) {
                    if ($(td).hasClass($(val).attr('sanitized'))) {
                        found.push($(td));
                    }
                    $(td).hide();
                    removeResult(td);
                }
            }
        });
        found.forEach(function (idx, val) {
            addResult(found[val]);
            $(found[val]).show(11);
        });
        $('a[id=resetFilters').text('Poista hakusuodattimet');
        $('a[id=resetFilters').show();
        updateResults();
    });
    $('a[id=resetFilters]').on('click', function () {
        $(this).hide();
        var rows = $('#serviceTable tr');
        for (i = 0; i < rows.length; i++) {
            td = rows[i].getElementsByTagName('td')[0];
            if (td) {
                if($(td).hasClass('first-result')){$(td).removeClass('first-result')};
                addResult(td);
                $(td).show();
            }
        }
        $('#serviceSearch').val('');
        updateResults();
    });
});
$('.card-content.collapse').on('show.bs.collapse', function () {
    $(this).siblings('.card-header').addClass('active');
});

$('.card-content.collapse').on('hide.bs.collapse', function () {
    $(this).siblings('.card-header').removeClass('active');
});

