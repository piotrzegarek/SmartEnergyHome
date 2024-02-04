$(document).ready(function() {
    enableEdit();
    enableDelete();
    handleUpdate();
});

/**
 * Add on click event to edit button and set input values for given device.
 */
function enableEdit() {
    $(".edit-device-btn").on("click", function () {
        hideFormErrors();
        var deviceRow = $(this).parent().parent()
        var deviceId = deviceRow.data('id');

        deviceRow.find('.dev-data').each(function(_, el) {
            var name = $(el).data('name');
            var value = $(el).text();
            if ($(`#id_${name}`).is('select')) {
                var value = $(`#id_${name}`).find(`option:contains(${value})`).val();
            }
            $(`#id_${name}`).val(value);
        });

        $("#editDeviceModal").attr('data-id', deviceId);
        $("#editDeviceModal").modal('show');
    });
}

/**
 * Add on click event to delete button and set input values for given device.
 */
function enableDelete() {
    $(".delete-device-btn").on("click", function () {
        var deviceRow = $(this).parent().parent()
        var deviceId = deviceRow.data('id');
        var deviceName = deviceRow.find('.device-name').text();

        $("#deleteDeviceModal").attr('data-id', deviceId);
        $("#deleteName").text(deviceName);
        $("#deleteDeviceModal").modal('show');
    });
}

$('#deleteDeviceModal').on('hidden.bs.modal', function () {
    $("#deleteDeviceModal").attr('data-id', null);
    $("#deleteName").text("");
});

$('#confirmDelete').on("click", function () {
    var deviceId = $("#deleteDeviceModal").attr('data-id');
    var deviceType = window.location.pathname.split("/")[2];

    $.ajax({
        url: '/devices/delete',
        type: "DELETE",
        dataType: "json",
        data: JSON.stringify({
            device_id: deviceId,
            device_type: deviceType
        }),
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
        success: (data) => {
            $("#deleteDeviceModal").modal('hide');
            showPopup(data['msg']);
            removeDeviceRow(deviceId);
        },
        error: (error) => {
            $("#deleteDeviceModal").modal('hide');
            showPopup(error.responseJSON['msg']);
        }
      });
});

function removeDeviceRow(deviceId) {
    var removeRow = $(`.device-row[data-id=${deviceId}]`);
    removeRow.remove();
}

function handleUpdate() {
    $('#updateForm').submit(function (e) {
        e.preventDefault();
        hideFormErrors();
        var deviceId = $("#editDeviceModal").attr('data-id');
        formData = {"id": deviceId,};

        $("#updateForm").find('.form-control').each(function(_, el) {
            var name = $(el).attr('name');
            var value = $(el).val();
            formData[name] = value;
        });
        var deviceType = window.location.pathname.split("/")[2];

        $.ajax({
            url: '/devices/update/' + deviceType,
            type: "POST",
            dataType: "json",
            data: JSON.stringify(formData),
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            success: (data) => {
                $("#editDeviceModal").modal('hide');
                showPopup(data['msg']);
                updateDeviceRow(data['device_data']);
            },
            error: (error) => {
                if (error.status == 400) {
                    showFormErrors(error.responseJSON["errors"]);
                } else {
                    $("#editDeviceModal").modal('hide');
                    showPopup(error.responseJSON['msg']);
                }
            }
        });
    });
}

function updateDeviceRow(deviceData) {
    var deviceRow = $(`.device-row[data-id="${deviceData.id}"]`);

    for (var name in deviceData) {
        var value = deviceData[name];
        if (name == "id") {
            continue;
        } else if (name == "plan_period") {
            value = capitalizeFirst(value);
        }
        deviceRow.find(`.dev-data[data-name="${name}"]`).text(value);
    }
}

function showFormErrors(errorList) {
    for (var name in errorList) {
        $(`.errorlist[data-name="${name}"] li`).text(errorList[name]);
    }
}

function hideFormErrors() {
    $('.errorlist li').each(function (_, el) {
        $(el).text("");
    })
}

function capitalizeFirst(text) {
    return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
}
