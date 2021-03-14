# Advanced router for Polymer

Change multiple page sections dynamically based on application state. Easily bind url params to your elements.
Designed for single page applications -SPA using [Polymer](https://www.polymer-project.org/).

## Why app-states

app-states allows you to define application states and updatable page sections independently.
With the support of nested states and model inheritance only required sections are updated.
This is the best scenario for real single page applications.

Features
- Declarative application states using web components.
- Nested states supporting inheritance.
- Custom page sections and dynamic content loading.
- Automatic data binding to url params and custom models.

###  Online demo http://kalitte.github.io/polymer-router-demo/

## Getting stared

New to app-states ? Just have a look at [Articles](http://kalitte.github.io/polymer-router-demo/#/articles) and [Account](http://kalitte.github.io/polymer-router-demo/#/account) demo.

## Installation
[Download](https://github.com/Kalitte/app-states) or run `bower install app-states --save`.

## Configuration
app-states uses the Polymer library. Make sure you have [webcomponents.js](http://webcomponents.org/polyfills/) and [polymer.html](https://www.polymer-project.org/) included in your page.

```html
<!doctype html>
<html>

<head>
    <script src="/bower_components/webcomponentsjs/webcomponents.js"></script>
    <link rel="import" href="/bower_components/Polymer/Polymer.html">
    <link rel="import" href="/bower_components/app-states/app-states.html">
</head>

<body unresolved>

    <a href="#/">Go home</a>
    <a href="#/login">Go Login</a>

    <!-- Define sections you want to load dynamically -->
    <section id="nav" is="states-section"></section>
    <section id="page" is="states-section"></section>

    <!-- Define application states -->
    <app-states>
        <app-state id="home">
            <template target="#nav" is="states-template">
                <!-- When url is / load this content into #nav section -->
                Hi from nav!
            </template>

            <template target="#page" is="states-template">
                <!-- When url is / load this content into #page section -->
                Hi from home!
            </template>

            <app-state id="login">
                <template target="#page" is="states-template">
                    <!-- When url is /login load this content into #page section -->
                    Hi from login!
                </template>
                <!-- Inherit #nav content from home -->
            </app-state>
        </app-state>
    </app-states>

</body>
</html>
```

