// https://usefulangle.com/post/1/jquery-dragging-image-within-div

var _DRAGGGING_STARTED = 0;
var _LAST_MOUSEMOVE_POSITION = { x: null, y: null };
var _DIV_OFFSET = $('.image-container').offset();
var _CONTAINER_WIDTH;
var _CONTAINER_HEIGHT;
var _IMAGE_WIDTH;
var _IMAGE_HEIGHT;
var _IMAGE_LOADED = 0;

// Check whether image is cached or wait for the image to load 
// This is necessary before calculating width and height of the image
if ($('.drag-image').get(0).complete) {
    ImageLoaded();
}
else {
    $('.drag-image').on('load', function () {
        ImageLoaded();
    });
}

// Image is loaded
function ImageLoaded() {
    _IMAGE_WIDTH = $(".drag-image").width();
    _IMAGE_HEIGHT = $(".drag-image").height();

    _CONTAINER_WIDTH = $(".image-container").outerWidth();
    _CONTAINER_HEIGHT = $(".image-container").outerHeight();

    _IMAGE_LOADED = 1;
}

$('.image-container').on('mousedown', function (event) {
    /* Image should be loaded before it can be dragged */
    if (_IMAGE_LOADED == 1) {
        _DRAGGGING_STARTED = 1;

        /* Save mouse position */
        _LAST_MOUSE_POSITION = { x: event.pageX - _DIV_OFFSET.left, y: event.pageY - _DIV_OFFSET.top };
    }
});

$('.image-container').on('mouseup', function () {
    _DRAGGGING_STARTED = 0;
});

$('.image-container').on('mousemove', function (event) {
    if (_DRAGGGING_STARTED == 1) {
        var current_mouse_position = { x: event.pageX - _DIV_OFFSET.left, y: event.pageY - _DIV_OFFSET.top };
        var change_x = current_mouse_position.x - _LAST_MOUSE_POSITION.x;
        var change_y = current_mouse_position.y - _LAST_MOUSE_POSITION.y;

        /* Save mouse position */
        _LAST_MOUSE_POSITION = current_mouse_position;

        var thisImage = $(this).children(".drag-image").first();

        var img_top = parseInt(thisImage.css('top'), 10);
        var img_left = parseInt(thisImage.css('left'), 10);

        var img_top_new = img_top + change_y;
        var img_left_new = img_left + change_x;

        /* Validate top and left do not fall outside the image, otherwise white space will be seen */

        // var aesthetics = 0.5;

        // if (currentScale <= 1) {// left side of the window is on the image
        //     var leftSide = (img_left_new <= 0 && img_left_new >= -_IMAGE_WIDTH * aesthetics)
        //         ? true : false;

        //     // right side
        //     var rightSide = (img_left_new <= _CONTAINER_WIDTH * aesthetics && img_left_new >= 0)
        //         ? true : false;

        //     var topSide = (img_top_new <= 0 && img_top_new >= -_IMAGE_HEIGHT * aesthetics)
        //         ? true : false;

        //     var botSide = (img_top_new <= _CONTAINER_HEIGHT * aesthetics && img_top_new >= 0)
        //         ? true : false;
        // }
        // else // zoomed in
        // {
        //     leftSide = rightSide = topSide = botSide = true;
        // }

        // // perform change component wise
        // if (leftSide || rightSide)
        //     thisImage.css({ left: img_left_new + 'px' });
        // if (topSide || botSide)
        //     thisImage.css({ top: img_top_new + 'px' });

        thisImage.css({left: img_left_new + 'px', top: img_top_new + 'px'});
    }
});

// https://stackoverflow.com/a/42058518/12944664
var zoomSpeed = 0.1;
var currentScale = 1;
$(".image-container").on('wheel', function (event) {
    event.preventDefault(); // https://stackoverflow.com/a/7600806/12944664

    // deltaY obviously records vertical scroll, deltaX and deltaZ exist too.
    // this condition makes sure it's vertical scrolling that happened
    if (event.originalEvent.deltaY !== 0) {

        if (event.originalEvent.deltaY < 0) {
            // wheeled up => zoom out
            currentScale -= zoomSpeed;
        }
        else {
            // wheeled down => zoom in
            currentScale += zoomSpeed;
        }

        // bounds on the scale factor
        // greater than 10%
        currentScale = currentScale <= 0.1 ? 0.1 : currentScale;

        $(this).children(".drag-image").css("transform", "scale(" + currentScale + ")");
    }
});

$(".re-center-button").click(function(event) {
    // button shares a common parent with the image container
    $(this).parent().find(".drag-image").css({transform: "none", left: "0px", top: "0px"});
});