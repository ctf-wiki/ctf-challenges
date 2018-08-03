const rvnorm = require( 'randgen' ).rvnorm;
const fs = require( 'fs' )

const S_MAX = 265; // squareMax
const M_MAX = 250; // multiplyMax
const MIN = 200;

const getNoises = ( () => {

    let noises = rvnorm( 400, 0, 7 );

    return ( length ) => {
        let result = [];
        for ( let i = 0; i < length; i++ ) {
            result.push( noises[ ~~( Math.random() * noises.length ) ] );
        }
        return result;
    }

} )();

let data = [];

let readData = [];
let readNoises = rvnorm( 200, 0, 30 );
for ( let i = 0; i < 200; i++ ) {
    let base = 300;
    if ( i < 30 || i > 175 ) {
        base = 150;
    }

    readData.push( base + readNoises[ i ] )
}

const getBitWaves = ( () => {

    let square = [];
    let multiply = [];
    let none = [];

    for ( let i = 0; i < 50; i++ ) {
        square.push( S_MAX );
        multiply.push( M_MAX );
        none.push( MIN );
    }

    let bit0 = multiply.concat( none );
    let bit1 = square.concat( multiply, none );

    return ( bit = '0' ) => {

        let noises = getNoises( 150 );

        if ( bit === '0' ) {
            // return bit0;
            return bit0.map( ( item, i ) => {
                return Number( ( item + noises[ i ] ).toFixed( 3 ) );
            } )
        } else {
            // return bit1;
            return bit1.map( ( item, i ) => {
                return Number( ( item + noises[ i ] ).toFixed( 3 ) );
            } )
        }
    }

} )();

fs.readFile( './key.txt', 'utf8', function ( err, data ) {
    const key = data;
    let result = [];

    key.split( '' ).forEach( bit => {
        Array.prototype.push.apply( result, getBitWaves( bit ) )
    } );

    result = readData.concat( result );

    fs.readFile( './template.tpl', 'utf8', function ( err, data ) {
        const content = data.replace( /\{\{\#data\}\}/, JSON.stringify( result ) );

        fs.writeFile( './dist/index.html', content, function ( err ) {
            if ( err )
                console.error( err )
            console.log( '更新密钥成功' )
        } );
    } );
} );
