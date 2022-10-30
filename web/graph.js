function toGraph(episodes) {
    const data = episodes.map(episode => {
        const node = {
            data: {
                ...episode,
                name: episode.title
            },
            group: 'nodes'
        };

        const edges = episode['referenced_episodes'].map(related => (
            {
                data: {
                    id: `${episode.id} => ${related}`,
                    source: episode.id,
                    target: related
                },
                group: 'edges'
            })
        );

        return [node, ...edges];
    });
    return data.flat();
}

async function renderGraph() {
    const response = await fetch('../data/geschichte.json', {mode: 'no-cors'});
    const json = await response.json();
    const graph = toGraph(json);

    const cy = cytoscape({
        container: document.getElementById('cy'),

        layout: {
            name: 'circle'
        },

        style: [
            {
                selector: 'node',
                style: {
                    'height': 20,
                    'width': 20,
                    'background-color': '#d19000'
                }
            },
            {
                selector: 'edge',
                style: {
                    'curve-style': 'haystack',
                    'haystack-radius': 0,
                    'width': 5,
                    'opacity': 0.5,
                    'line-color': '#f2f08c'
                }
            }
        ],

        elements: graph
    });
}

document.addEventListener('DOMContentLoaded', () => {
    renderGraph();
});
