$(".delete-device-btn").on("click", function () {
    var deviceRow = $(this).parent().parent()
    var deviceId = deviceRow.data('id');
    var deviceName = deviceRow.find('.device-name').text();

    $("#deleteDeviceModal").attr('data-id', deviceId);
    $("#deleteName").text(deviceName);
    $("#deleteDeviceModal").modal('show');
});

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
