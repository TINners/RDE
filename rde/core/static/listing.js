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

    function selectedTheses() {
        return $('.thesis :checkbox:checked').map(function() {
            return this.value
        }).get();
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

    // Bind event handlers:
    bindAllCheckbox();
    bindEdit();
    bindDelete();
    bindCreate();
});

