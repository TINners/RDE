// On document ready...
$(function() {
    // Involved elements:
    var $getXML = $('#get-xml-btn');
    var $create = $('#create-btn');
    var $edit = $('#edit-btn');
    var $del = $('#delete-btn');
    var $all = $(':checkbox[value="all"]');
    var $theses = $('.thesis :checkbox');

    // POST form template - used as a base for generated temporary forms.
    var $formTemplate = $('#form-template');

    function bindAllCheckbox() {
        // Toggle all checkboxes when "all" is toggled.
        $all.on("change", function() {
            var select = $(this).is(":checked");

            $theses.prop("checked", select).trigger("change");
        });
    }

    function bindEdit() {
        // Update activity when checkbox' state changes.
        $theses.on("change", updateEditActivity);

        // Redirect to the modification form when clicked.
        $edit.on("click", redirectToEdit);
    }

    function bindDelete() {
        // Update activity when checkbox' state changes.
        $theses.on("change", updateDeleteActivity);

        // Post deletion to the server (after confirmation) when clicked.
        $del.on("click", confirmDelete);
    }

    function bindCreate() {
        // Create is always active and redirects to the thesis creation form.
        $create.on("click", redirectToCreate);
    }

    function bindExport() {
        // Update activity when checkbox' state changes.
        $theses.on("change", updateExportActivity);

        // Post and export request to the server when clicked.
        $getXML.on("click", postExport);
    }

    function updateEditActivity() {
        // "Edit" is only active when there is exactly one checkbox selected.
        if (selectedTheses().length == 1) {
            $edit.prop("disabled", null);
        }
        else {
            $edit.prop("disabled", "disabled");
        }
    }

    function updateDeleteActivity() {
        // "Delete" is active if there is at least one checkbox selected.
        if (selectedTheses().length > 0) {
            $del.prop("disabled", null);
        }
        else {
            $del.prop("disabled", "disabled");
        }
    }

    function updateExportActivity() {
        // Export is only active if there is at least one selected thesis
        // AND if all selected theses are of the same kind.
        var theses = selectedTheses();

        if (theses.length > 0 && sameKind(theses)) {
            $getXML.prop("disabled", null);
        }
        else {
            $getXML.prop("disabled", "disabled");
        }
    }

    function selectedTheses() {
        return $('.thesis :checkbox:checked').map(function() {
            return this.value
        }).get();
    }

    function sameKind(theses) {
        if (!theses.length) {
            return true
        }

        var first = theses[0];
        var desiredKind = $('.thesis:has(:checkbox[value="' + first + '"])').data("kind");

        return ($('.thesis:has(:checkbox:checked)')
            .filter(function() { return $(this).data("kind") != desiredKind })
            .length == 0);
    }

    function redirectToEdit() {
        window.location = "/thesis/" + selectedTheses()[0] + "/";
    }

    function redirectToCreate() {
        window.location = "/thesis/create/";
    }

    function confirmDelete() {
        if (confirm("Czy na pewno chcesz usunąć zaznaczone pozycje?")) {
            post("/thesis/delete/", {ids: selectedTheses().join()});
        }
    }

    function postExport() {
        post("/export/", {ids: selectedTheses().join()});
    }

    function post(url, data) {
        var form = $formTemplate.clone();
        form.prop("action", url);

        $.each(data, function(key, val) {
            form.append($('<input type="hidden" name="' + key + '" value="' + val + '"/>'));
        });

        form.appendTo('body').submit();
    }

    // Set initial button enabled state:
    updateEditActivity();
    updateDeleteActivity();
    updateExportActivity();

    // Bind event handlers:
    bindAllCheckbox();
    bindEdit();
    bindDelete();
    bindCreate();
    bindExport();
});

