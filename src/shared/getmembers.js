import { selectedYear, congressData } from "./dataManager.js";

//takes year and chamber (senate or house) and gets every member that served that year
export function getMembersFromYear(chamber, year, data) {
    console.log('getMembersFromYear called', { chamber, year });
    if (!data) {
        console.log('getMembersFromYear: no data passed');
        return [];
    }

    // normalize data: some files may wrap the array in an object
    let members = data;
    if (!Array.isArray(members) && typeof members === 'object') {
        members = members.members || members.data || members.results || Object.values(members)[0] || [];
    }

    const congressNumberThatYear = Math.ceil((year - 1788) / 2);
    console.log('getMembersFromYear: congressNumberThatYear=', congressNumberThatYear, 'membersCount=', Array.isArray(members) ? members.length : 0);

    return (Array.isArray(members) ? members : []).filter(member => {
        let servedYear = false;
        if (!member || !Array.isArray(member.terms)) return false;
        member.terms.forEach(term => {
            // allow chamber === "Both" to match any chamber, and use loose equality for congress
            if ((chamber === 'Both' || term.chamber === chamber) && term.congress == congressNumberThatYear) {
                servedYear = true;
            }
        })
        return servedYear;
    })
}

//returns a list of the years served in the house and senate for each congress member
export function getYearsServed(year, data) {

    console.log(data);

    const congressNumberThatYear = Math.ceil((year - 1788) / 2);
    return data.map(member => {
        let houseYears = 0;
        let senateYears = 0;

        member.terms.forEach(term => {
            if (term.congress <= congressNumberThatYear) {
                let yearsServedThatTerm = term.endYear - term.startYear;
                term.chamber === "Senate" ? senateYears += yearsServedThatTerm : houseYears += yearsServedThatTerm;
            }
        })

        //list position 1 is age,  2 is house, position 3 is senate
        return [member.name, year - member.yob, houseYears, senateYears]
    })
}

export function getMembersYearsServed(year, data) {

    console.log(data);

    const congressNumberThatYear = Math.ceil((year - 1788) / 2);

    let houseYears = 0;
    let senateYears = 0;

    data.terms.forEach(term => {
        if (term.congress <= congressNumberThatYear) {
            let yearsServedThatTerm = term.endYear - term.startYear;
            term.chamber === "Senate" ? senateYears += yearsServedThatTerm : houseYears += yearsServedThatTerm;
        }
    })

    console.log(houseYears);
    const person = {house: houseYears, senate: senateYears}

    return {house: houseYears, senate: senateYears}
}