#might have to edit url


#for multiple diets & health
$('#search-filter-diet').find("ul li").each(function() {
		if($(this).hasClass('selected')){
			
			if ($(this).find('input').filter('[name="health"]').length > 0) {
				dietURLParam += '&health='+$(this).find('input[name="health"]').val();
			}				
							
			if ($(this).find('input').filter('[name="diet"]').length > 0) {
				allerURLParam += '&diet='+$(this).find('input[name="diet"]').val();
			}
			
		}
	});

#multiple ingredients
var url = response.hits[i].recipe.label;
    url = url.split(" ").join("-").toLowerCase();
    url = url+'-'+uri;
    url = '../recipe/?recipe='+url+'/search='+q.replace(" ", "+");

#take form data split by comma, change to array?