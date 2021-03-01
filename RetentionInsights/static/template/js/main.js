$(window).on("load", function () {
    
    /*==================================================================
    [ Focus]*/

    /*---------------------------------
    Explanation:
    1. Get all the question container divs first.
    2. Loop through each question container.
    3. In the current container (parent), get the children inputs: (either text, slider, or radio) 
    4. Loop through each input element and add the appropriate event listener.
    5. On action, add the 'has-val' class to the parent - the CSS takes care of the animation
    This makes it easier to display the completion animation and check for completion on submit
    ---------------------------------*/
    
    //Get all the question containers
    $('.questionContainer').each(function(){
        var parent = $(this); //Current parent div 
        var text = parent.find('.input100'); //Includes short and long text
        var sliders = parent.find('.slider100');
        var radios = parent.find('.radio100');

        /* -- Short and Long Text -- */
        if (text.length > 0) {
            text.each(function(){
                $(this).on('focus', function(){ //Animate on focus
                    parent.addClass('has-focus');
                });
                
                $(this).on('blur', function(){ //Validate on blur
                    if($(this).val().trim() != "") { //If the value is not empty
                        parent.addClass('has-val');
                    }
                    else {
                        parent.removeClass('has-val');
                        parent.removeClass('has-focus');
                    }
                });    
            });
        }

        /* -- Sliders -- */
        if (sliders.length > 0) {
            sliders.each(function(){ 
                $(this).on('input', function(){ //Triggers when the slider is moved
                    if($(this).val() != "4") { //If the value is not null (4 = null)
                        parent.addClass('has-val');
                    }
                    else {
                        parent.removeClass('has-val');
                    }
                });    
            });
        }

        /* -- True or False -- */
        if (radios.length > 0) {
            radios.each(function () {
                $(this).on('change', function(){
                    parent.addClass('has-val');
                });
            });
        }
        
    });    
    
    /*==================================================================
    [ Validation Functions ]*/
    
    //Validate on Submit
    $('#survey-form').on('submit',function(){
        //Initialize to is Valid
        isValid = true;

        //Get all the questions and check for the "has-val" class
        $('.questionContainer').each(function () {
            //If not, showValidate and make survey not valid
            if (!$(this).hasClass('has-val')) {  
                showValidate($(this));
                isValid = false;

                //Add 'has-error' to grandparentparent of questionContainer (container-contact)
                $(this).parent().parent().addClass('has-error');

            }
        });

        if (isValid == false) {
            $('html, body').animate({
                    scrollTop: ($('.has-error').first().offset().top)
                },100);   
            }

        return isValid;
    });

    //Hide Validation on focus for text areas on focus
    $('.input100').each(function(){
        $(this).focus(function(){
            //For text areas, the questionContainer is the immediate parent
            questionContainer = $(this).parent();

            hideValidate(questionContainer);
       });
    });

    //Hide Validation on change for sliders on input
    $('.slider100').each(function(){
        $(this).on('input', function(){
            //For sliders, the questionContainer is the immediate parent
            questionContainer = $(this).parent();

            hideValidate(questionContainer);
       });
    });

    //Hide Validation on change for radio on change
    $('.radio100').each(function(){
        $(this).on('change', function(){
            //For radios, the questionContainer is the TWO parents above
            questionContainer = $(this).parent().parent();

            hideValidate(questionContainer);
       });
    });

    //Show Validation Message : Receives the questionContainer div.
    function showValidate(questionContainer) {
        //Grabs the div above questionContainer (wrap-input div)
        var wrapInput = $(questionContainer).parent();
        
        //This triggers the red line animation on the following span (CSS)
        $(wrapInput).addClass('alert-validate');


        //This Grabs the parent of wrapInput -> wrap-contact100
        var parent = wrapInput.parent();

        // Find the alert span and triggers alert sign
        var displayAlert = parent.find('.alert-input100');
        $(displayAlert).addClass('display-alert-sign');

        // Bring focus to the error
        wrapInput.focus();

    }

    //Hides Validation : Receives the questionContainer div.
    function hideValidate(questionContainer) {
        //Grabs the div above questionContainer (wrap-input div)
        var wrapInput = $(questionContainer).parent();
        
        //Removes alert class
        $(wrapInput).removeClass('alert-validate');
        
        //This Grabs the parent of wrapInput -> wrap-contact100
        var parent = wrapInput.parent();
        
        // Find the alert span and remove alert sign adn has-error class
        var displayAlert = parent.find('.alert-input100');
        $(displayAlert).removeClass('display-alert-sign');
        $(parent).removeClass('has-error');
    }
    
});