app.Play = Backbone.Collection.extend({
    model: app.Letter,


    initialize: function() {
        // remove letters that are no longer in play
        // this.listenTo(this, 'change:inPlay', this.updatePositions);
    },


    toString: function() {
        var word = '';

        // construct the letters into a string
        this.each(function(letter) {
            word += letter.get('character');
        });

        return word;
    },


    updatePositions: function() {
        // console.log('change');
    }


    /*
    validate: function() {
        var errors;

        // make sure the dictionary is loaded 
        if (typeof(scrabble_dict) != 'undefined') {
            var word = this.toString();

            // word is in dictionary?
            if (_.indexOf(scrabble_dict, word, true) === -1) {
                errors = word + ' is not in the dictionary.'    
            }

            // length?
            if (word.length < 2) {
                errors = 'words must be at least 2 letters.';
            }

            // word has not been used before?
            _.each(this.playedOut, function(w) {
                if (word == w || word.pluralize() == w || word.singularize() == w) {
                    errors = 'you may not play a word that has been used before.';
                }
            });
        }
        else {
            errors = 'dictionary is loading; please wait and try again.';
        }

        return errors;
    },
    */



});
