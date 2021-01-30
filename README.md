# SWE 573 Reddit Analyzer Software Solution Project




<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
![Login Page](https://github.com/hseyindemir/swe_773_hdemir/blob/main/documents/project-1.png)

There are many great README templates available on GitHub, however, I didn't find one that really suit my needs so I created this enhanced one. I want to create a README template so amazing that it'll be the last one you ever need -- I think this is it.

Here's why:
* Your time should be focused on creating something amazing. A project that solves a problem and helps others
* You shouldn't be doing the same tasks over and over like creating a README from scratch
* You should element DRY principles to the rest of your life :smile:

Of course, no one template will serve all projects since your needs may be different. So I'll be adding more in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue. Thanks to all the people have have contributed to expanding this template!

A list of commonly used resources that I find helpful are listed in the acknowledgements.

### Built With

This section should list any major frameworks that you built your project using. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.
* [Python](https://getbootstrap.com)
* [React](https://jquery.com)
* [PostgreSQL](https://laravel.com)



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* docker
* python
* nodejs
* postgresql

### Installation
* clone the repository into local computer
```sh
  git clone https://github.com/hseyindemir/swe_773_hdemir.git
```
* go to projectBase directory on the clonned project and run the database environment
```sh
cd projectBase
docker build -t reddit_pg_container ./database_infrastructure
docker run -d --name reddit_db -p 5432:5432 reddit_pg_container
```
* run the application
```sh
docker build -t swe573_reddit:v3 .
docker run -dit --rm -p 5000:5000 --name swe573_backend --link reddit_db swe573_reddit:v3
```
* run the frontend
  
```sh
cd swe_773_hdemir\frontend
docker build -t swe573_fe:v2 .
docker run -dit --rm -p 3000:3000 --name swe573_fe swe573_fe:v2
```

<!-- USAGE EXAMPLES -->
## Usage

After installing the project you can use this frontend enpoint in order to test and see the application

http://localhost:3000/



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/hseyindemir/swe_773_hdemir/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Hüseyin Demir - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/hseyindemir/swe_773_hdemir](https://github.com/hseyindemir/swe_773_hdemir)
