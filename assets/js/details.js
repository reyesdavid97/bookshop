Vue.component('star-rating', {
  template: `<div class="rating-input rating">
      <span v-for="(_, index) in possible" class="star mr-1">
        <i v-if="index < rating" v-on:click="onRate(index + 1)" class="fa fa-star"></i>
        <i v-if="index >= rating" v-on:click="onRate(index + 1)" class="fa fa-star-o"></i>
      </span>
  </div>`,

  data: function() {
    return {
      possible: 5,      
      rating: 0,
    }
  },

  computed:{
    active: function() {
      return this.rating;
    },
    inactive: function() {
      return this.possible - this.rating;
    }
  },

  methods: {
    onRate: function(index) {
      this.rating = index;
      this.$emit('ratingchange', this.rating);
    } 
  }
})

var detailsApp = new Vue({
  el: '#panel4',
  delimiters: ["{-", "-}"],
  data: {
    book_id: null,
    rating: 0,
    comments: '',
    commentLimit: 250,
    anonymous: false,

    loading: false
  },

  computed: {
    allowSubmit: function() {
      return this.comments.trim().length > 0 || this.rating != 0
    },
    remainintChars: function() {
      return this.commentLimit - this.commentText.length;
    },
    commentText: function() {
      return this.comments.substr(0, this.commentLimit);
    }
  },

  methods: {
    onSubmit: function(event) {
      var self = this;
      event.preventDefault();

      var review_data = {
        rating: self.rating,
        comments: self.comments,
        anonymous: self.anonymous
      };

      $.ajax({
        type:"POST",
        url: detailsObject.review_url,
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(review_data)
      }).done(function(response) {
        if (response.indexOf("Saved") >= 0) {
          window.location.reload();
        }
        else {
          console.log(response);
        }
      }).error(function(error) {
        alert(error.responseText);
      });
    },
    onCommentChange: function(event) {
      var val = event.target.value;
      this.comments = val;
    },
    onRatingChange: function(rating) {
      this.rating = rating;
    }
  }
})

