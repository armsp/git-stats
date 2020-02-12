import { request } from "https://cdn.pika.dev/@octokit/request";
myAsyncMethod();
async function myAsyncMethod() {
    const result = await request("POST /graphql", {
        headers: {
            authorization: "token 308a6a514d787cdf55cea98f883294bb8d94ba80"
        },
        query: `query {
                    viewer{
                        repositories(orderBy: {field: STARGAZERS, direction: DESC}){
                        totalCount
                        }
                        followers{
                        totalCount
                        }
                        issues_sum:issues{
                        totalCount
                        }
                        issues_open:issues(states: OPEN){
                        totalCount
                        }
                        issues_closed:issues(states: CLOSED){
                        totalCount
                        }
                        pr_sum:pullRequests{
                        totalCount
                        }
                        pr_open:pullRequests(states: OPEN){
                        totalCount
                        }
                        pr_closed:pullRequests(states: CLOSED){
                        totalCount
                        }
                        pr_merged:pullRequests(states: MERGED){
                        totalCount
                        }
                        repositories(orderBy: {field: STARGAZERS, direction: DESC}){
                        nodes{
                            name
                            stargazers{
                            totalCount
                            }
                            watchers{
                            totalCount
                            }
                            forkCount
                        }
                        }
                    }
                    }`
    });
    // console.log(`${result.data.length} repos found.`);
    console.log("Repo Count: ", result.data.data.viewer.repositories.totalCount);
    console.log("Followers: ", result.data.data.viewer.followers.totalCount);
    console.log("Open Issues: ", result.data.data.viewer.issues_open.totalCount);
    console.log("CLosed Issues: ", result.data.data.viewer.issues_closed.totalCount);
    console.log("PR Open: ", result.data.data.viewer.pr_open.totalCount);
    console.log("PR Closed: ", result.data.data.viewer.pr_closed.totalCount);
    console.log("PR Merged: ", result.data.data.viewer.pr_merged.totalCount);
    // console.log("Repo Count: ", result.data.data.viewer.repositories.nodes.length);
    var stargazers = 0, watchers = 0, forks = 0, i;
    for (i = 0; i < result.data.data.viewer.repositories.nodes.length; i++) {
        stargazers += result.data.data.viewer.repositories.nodes[i].stargazers.totalCount;
        watchers += result.data.data.viewer.repositories.nodes[i].watchers.totalCount;
        forks += result.data.data.viewer.repositories.nodes[i].forkCount;
    }
    console.log("Stars: ", stargazers);
    console.log("Watchers: ", watchers);
    console.log("Forks: ", forks);
    // document.getElementById("result").innerHTML = JSON.stringify(result.data, null, '\t');
    document.getElementById("star").innerHTML = stargazers;
    document.getElementById("follower").innerHTML = result.data.data.viewer.followers.totalCount;
    document.getElementById("pr").innerHTML = result.data.data.viewer.pr_open.totalCount;
    document.getElementById("o-iss").innerHTML = result.data.data.viewer.issues_open.totalCount;
    document.getElementById("c-iss").innerHTML = result.data.data.viewer.issues_closed.totalCount;
    document.getElementById("fork").innerHTML = forks;
    document.getElementById("watcher").innerHTML = watchers;
    document.getElementById("repo").innerHTML = result.data.data.viewer.repositories.totalCount;
}