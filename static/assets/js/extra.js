"use strict";
$(document).ready(function () {
$("#basic-datatables").DataTable({});

$("#multi-filter-select").DataTable({
    pageLength: 15,
    initComplete: function () {
    this.api()
        .columns()
        .every(function () {
        var column = this;
        var select = $(
            '<select class="form-select"><option value=""></option></select>'
        )
            .appendTo($(column.footer()).empty())
            .on("change", function () {
            var val = $.fn.dataTable.util.escapeRegex($(this).val());

            column
                .search(val ? "^" + val + "$" : "", true, false)
                .draw();
            });

        column
            .data()
            .unique()
            .sort()
            .each(function (d, j) {
            select.append(
                '<option value="' + d + '">' + d + "</option>"
            );
            });
        });
    },
});

// For Individual Deposits Total Filter
$("#multi-filter-select-individual-deposit").DataTable({
    pageLength: 15
});
// Add Row
// $("#add-row").DataTable({
//     pageLength: 5,
// });

var action =
    '<td> <div class="form-button-action"> <button type="button" data-bs-toggle="tooltip" title="" class="btn btn-link btn-primary btn-lg" data-original-title="Edit Task"> <i class="fa fa-edit"></i> </button> <button type="button" data-bs-toggle="tooltip" title="" class="btn btn-link btn-danger" data-original-title="Remove"> <i class="fa fa-times"></i> </button> </div> </td>';

$("#addRowButton").click(function () {
    $("#add-row")
    .dataTable()
    .fnAddData([
        $("#addName").val(),
        $("#addPosition").val(),
        $("#addOffice").val(),
        action,
    ]);
    $("#addRowModal").modal("hide");
});
});




// For Login Page Only
(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$(".toggle-password").click(function() {

	  $(this).toggleClass("fa-eye fa-eye-slash");
	  var input = $($(this).attr("toggle"));
	  if (input.attr("type") == "password") {
	    input.attr("type", "text");
	  } else {
	    input.attr("type", "password");
	  }
	});

})(jQuery);