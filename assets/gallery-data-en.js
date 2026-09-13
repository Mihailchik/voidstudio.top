const galleryEnglishCopy = {
  1: {title:'Beyond',category:'Space · Video',description:'Space begins where familiar points of reference disappear.',role:'Published work · generation and animation · 2026',urlLabel:'View publication'},
  29: {title:'Bird in a Golden Field',category:'Painterly experiment',description:'A bird, a golden field and barbed wire bring the living world up against an artificial boundary.',role:'Published work · generation · 2026',urlLabel:'View publication'},
  30: {title:'Red Horizon',category:'Space · Concept',description:'One figure faces the unknown. Scale emerges from red light and the depth of a dark space.',role:'Published work · generation · 2026',urlLabel:'View publication'},
  32: {title:'Rose of Memory',category:'Visual image',description:'One colour stays alive in the cold space of memory.',role:'Published work · generation · 2026',urlLabel:'View publication'},
  37: {title:'Pizza by the Fire',category:'Food · Image',description:'Pizza shown through the craft behind it: oven, smoke, charred dough and open flame.',role:'Original work · generation'},
  38: {title:'Heat of the Oven',category:'Food · Image',description:'A close product shot built around a hot crust, melted cheese and the glow of the oven.',role:'Original work · generation'},
  63: {title:'Light and Shadow',category:'Observation · Image',description:'Human silhouettes and hard sunlight form an almost abstract rhythm.',role:'Photo study · Void Studio'},
  101: {title:'At the Water’s Edge',category:'Nature · Image',description:'A low viewpoint, wet rocks and the small owner of the shore.',role:'Original work · generation'},
  102: {title:'Quiet Screening',category:'Editorial image',description:'A pause between the action on screen and the viewer’s own thoughts.',role:'Original work · generation'},
  103: {title:'The Railway Quarter',category:'Travel · Photography',description:'Here the railway is a street, a route and the axis of the neighbourhood at once.',role:'Photography · Hugo Guillemard / Pexels'},
  104: {title:'Hot Toast',category:'Food · Image',description:'An advertising food shot: crisp crust, flowing yolk and a close study of texture.',role:'Original work · generation'},
  105: {title:'Sunflower',category:'Nature · Image',description:'A warm flower, muted green and a hand entering the lower edge of the frame.',role:'Image · visual curation'},
  106: {title:'Time on the Road',category:'Graphic · Image',description:'A motorcycle and a clock merge into a single sign of movement.',role:'Original work · generation'},
  107: {title:'Cold Morning',category:'Nature · Video',description:'A white cat moves through cold, diffused morning light.',role:'Original work · generation and animation'},
  108: {title:'White Cat at Sunset',category:'Nature · Video',description:'The same scene at sunset, shifting from a cold atmosphere to low warm light.',role:'Original work · generation and animation'},
  109: {title:'The Last Message',category:'Illustration · Video',description:'A message arrives when there is no one left to answer it.',role:'Original work · generation and animation'},
  110: {title:'The Rider and the Fish',category:'Illustration · Video',description:'An adventure illustration built around a deliberately impossible catch.',role:'Original work · generation and animation'},
  111: {title:'Under Sail',category:'Travel · Video',description:'Wind, water and working sails, seen from a moving deck.',role:'Original work · generation and animation'},
  201: {title:'After Midnight',category:'Street food · Concept',description:'Not simply late-night food, but warmth, closeness and the company worth coming back for.',role:'Original concept · idea, art direction, generation · 2025'},
  202: {title:'The Passage',category:'Editorial image',description:'The subject moves through a corridor of other people’s attention and expectation.',role:'Original concept · idea, art direction, generation · 2025'},
  203: {title:'Voltage Field',category:'Cover · Concept',description:'Artwork for an electronic release about systems that wake before the city and outlast the people inside it.',role:'Original concept · idea, art direction, generation · 2025'},
  204: {title:'Sea Buckthorn No. 14',category:'Packaging · Concept',description:'A seasonal drink concept combining sea-buckthorn colour, watercolour and Japanese poster graphics.',role:'Original concept · idea, art direction, generation · 2025'},
  205: {title:'Precision Cut',category:'Brand image · Concept',description:'A barbershop image focused on the craft, concentration and trust behind the haircut.',role:'Original concept · idea, art direction, generation · 2025'},
  206: {title:'Small System',category:'Editorial macro',description:'A cover image about the small systems that hold up a much larger ecosystem.',role:'Original concept · idea, art direction, generation · 2025'},
  207: {title:'Held Breath',category:'Graphic · Study',description:'A single contour in place of a finished portrait: one gesture and a brief pause.',role:'Original concept · graphic, generation · 2025'},
  208: {title:'The Painting Looks Back',category:'Illustration series',description:'A concept for an art school in which the character stops being a drawing and answers its creator.',role:'Original concept · idea, art direction, generation · 2025',frames:[{src:'../assets/gallery/first-viewer.webp',label:'The first viewer'},{src:'../assets/gallery/painting-looks-back.webp',label:'A conversation with the painting'}]},
  209: {title:'The Right to Disconnect',category:'Technology poster',description:'A campaign for the right to be offline. Connection becomes a trace someone has chosen to leave behind.',role:'Original concept · idea, art direction, generation · 2025'},
  210: {title:'Green Ritual',category:'Still-life series',description:'Two states of matcha: dry powder and a hot drink. Texture carries the quiet rhythm of the ritual.',role:'Original concept · idea, art direction, generation · 2025',frames:[{src:'../assets/gallery/green-ritual-powder.webp',label:'Material'},{src:'../assets/gallery/green-ritual-tea.webp',label:'Ritual'}]}
};

galleryWorks.forEach(work => {
  if (galleryEnglishCopy[work.id]) Object.assign(work, galleryEnglishCopy[work.id]);
  work.src = work.src.replace(/^assets\//, '../assets/');
  if (work.poster) work.poster = work.poster.replace(/^assets\//, '../assets/');
  if (work.frames && !galleryEnglishCopy[work.id]?.frames) {
    work.frames = work.frames.map(frame => ({...frame, src: frame.src.replace(/^assets\//, '../assets/')}));
  }
});
