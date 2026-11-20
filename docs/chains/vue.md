# Vue Cinemas API Documentation

Endpoints and response formats for retrieving cinema, film, and showing data from Vue Cinemas.

## Headers & Authorisation

All requests to `/api/microservice/...` endpoints require an authentication token and standard JSON headers.

| Header | Value |
| :--- | :--- |
| `User-Agent` | `showtime-scraper/0.1 (+https://github.com/AlexGordon0/showtime)` |
| `Accept` | `application/json` |
| `Authorization` | `Bearer {microservicesToken}` |

### Acquiring a Token

A `{microservicesToken}` can be acquired by sending an initial request to `GET https://www.vue.com`. 
The token is returned in the response headers (via `set-cookie` as `microservicesToken=...`).


## Fetch List of Cinemas

Endpoints which return a list of cinemas.

### Endpoints

#### `GET https://www.myvue.com/api/microservice/showings/cinemas` 

Retrieves all available Vue cinemas grouped alphabetically.

#### `GET https://www.myvue.com/api/microservice/showings/cinemas?filmId={filmId}`

Retrieves all cinemas currently screening a given film.

- **Example Request:** `GET https://www.myvue.com/api/microservice/showings/cinemas?filmId=HO00021363`

##### Query Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `filmId` | `str` | **Yes** | The unique ID of the film (matches `filmId` from the films endpoint). |

### Example Response

```json
{
    "result": [
        {
            "alpha": "A",
            "cinemas": [
                {
                    "cinemaId": "10051",
                    "cinemaName": "Accrington",
                    "fullName": "Accrington - The Viaduct",
                    "venueCurrency": "GBP",
                    "itemName": "Accrington",
                    "whatsOnUrl": "https://www.myvue.com/cinema/accrington/whats-on",
                    "isSecondaryMarket": false,
                    "prolongingBookingTimer": 20
                }
            ]
        }
    ],
    "responseCode": 0,
    "errorMessage": null
```

### Top-Level Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `result` | `list` | List of alphabetical cinema groups (`alpha` + `cinemas`). |
| `responseCode` | `int` | `0` indicates success; non-zero indicates an error. |
| `errorMessage` | `str \| null` | Error details when `responseCode` is non-zero. |

### Cinema Object Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `cinemaId` | `str` | Unique identifier for the cinema. |
| `cinemaName` | `str` | Shortened display name of the cinema. |
| `fullName` | `str` | Full name of the venue. |
| `venueCurrency` | `str` | ISO currency code used at the venue. |
| `itemName` | `str` | Usually matches `cinemaName`. |
| `whatsOnUrl` | `str` | URL to the branch's What's On page. |
| `isSecondaryMarket` | `bool` | `true` for venues outside Great Britain. |
| `prolongingBookingTimer` | `int` | Booking hold/extend duration in seconds. |


## Fetch List of Films

Endpoints which return a list of films.

### Endpoints

#### `GET https://www.myvue.com/api/microservice/showings/films` 

Retrieves all films currently showing in Vue cinemas.

#### `GET https://www.myvue.com/api/microservice/showings/films?cinemaId={cinemaId}` 

Retrieves all films currently screening in a given cinema.

- **Example Request:** `GET https://www.myvue.com/api/microservice/showings/films?cinemaId=10051` 

##### Query Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `cinemaId` | `str` | **Yes** | The unique ID of the cinema (matches `cinemaId` from the cinema endpoint). |

### Example Response

```json
{
    "result": [
        {
            "filmId": "HO00020283",
            "certificate": {
                "name": "12a",
                "description": "Suitable for people aged 12 and over. Younger children will not be able to attend unless accompanied by an adult.",
                "src": "https://www.myvue.com/-/media/vuecinemas/certificates/uk/12a.png?rev=b91ed3a02335433fb5f5becf370850dc&sc_lang=en"
            },
            "secondaryCertificates": [],
            "filmUrl": "https://www.myvue.com/film/the-hunger-games-sunrise-on-the-reaping",
            "filmAttributes": [],
            "posterImageSrc": "https://www.myvue.com/-/media/vuecinemas/img/import/4e807691-17ef-406a-8ef8-a5bdff8b4e3c_the-hunger-games-sunrise-on-the-reaping_posters_gb_english_sols.jpg?rev=531c4e48f6bb4f7087b26f94435591ac",
            "cast": "Joseph Zada, McKenna Grace, Jesse Plemons, Elle Fanning, Ralph Fiennes, Glenn Close, Maya Hawke, Kieran Culkin",
            "releaseDate": "2026-11-18T00:00:00",
            "runningTime": 158,
            "isDurationUnknown": false,
            "synopsisShort": "The Hunger Games: Sunrise on the Reaping will revisit the world of Panem twenty-four years before the events of The Hunger Games, starting on the morning of the reaping.",
            "filmTitle": "The Hunger Games: Sunrise On The Reaping",
            "hasSessions": true,
            "hasTrailer": true,
            "embargoMessage": null,
            "embargoEndDate": null,
            "embargoLevel": null,
            "priceMessage": "",
            "alternativeCertificate": {
                "name": null,
                "description": null,
                "src": null
            },
            "panelImageUrl": "https://www.myvue.com/-/media/vuecinemas/img/import/0b50e023-aa83-4a2c-95d9-51527244a410_the-hunger-games-sunrise-on-the-reaping_stills_solstice_unit_25.jpg?rev=7f14eb8326d54c478b0f1c0c544f8af7",
            "filmStatus": 1,
            "trailers": [],
            "director": "Francis Lawrence",
            "distributor": "Lionsgate (UK + EIRE)",
            "movieXchangeCode": "0e12957f-3dc2-4ebd-be6a-23fcc1736399",
            "crossCountryMovieXchangeId": "266a2e58-59a7-48f9-b107-0cf112c1b6cc",
            "originalTitle": "The Hunger Games: Sunrise on the Reaping",
            "showingInCinemas": [
                "10003", "10076", "10086", "10097", "10089", "10059", "10096",
                "10010", "10069", "10011", "10041", "10090", "10044", "10067",
                "10025", "10060", "10034", "10075", "10068", "10056", "10006",
                "10019", "10018", "10040", "10015", "10055", "10087", "10092",
                "10029", "10078", "10094", "10063", "10099", "10077", "10070",
                "10066", "10057", "10091", "10071", "10030", "10080", "10046",
                "10031", "10022", "10026", "10012", "10037", "10079", "10061",
                "10049", "10065", "10035", "10048", "10017", "10023", "10084",
                "10058", "10083", "10024", "10004", "10042", "10050", "10020",
                "10043", "10021", "10027", "10008", "10014", "10005", "10053",
                "10073", "10064", "10081", "10074", "10072", "10095", "10051",
                "10088", "10085", "20004", "10032", "10007", "10038", "10098",
                "20003", "20000", "20002", "10013", "10093", "10001", "10045"
            ],
            "genres": [
                "Fantasy"
            ],
            "sessionAttributes": []
        }
    ],
    "responseCode": 0,
    "errorMessage": null
}
```

### Top-Level Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `result` | `list` | List of film objects |
| `responseCode` | `int` | `0` indicates success; non-zero indicates an error. |
| `errorMessage` | `str \| null` | Error details when `responseCode` is non-zero. |

### Film Object Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `filmId` | `str` | Unique identifier for the film. |
| `certificate` | `object` | Primary age rating object (see below). |
| `secondaryCertificates` | `list` | Additional age ratings or regional certificates, if applicable. |
| `filmUrl` | `str` | Direct URL to the film's page on the Vue website. |
| `filmAttributes` | `list` | Special tags or accessibility/format attributes associated with the film. |
| `posterImageSrc` | `str` | URL to the vertical poster artwork for the film. |
| `cast` | `str` | Comma-separated list of main cast members. |
| `releaseDate` | `str` | ISO 8601 datetime string of the film's release date. |
| `runningTime` | `int` | Runtime of the film in minutes. |
| `isDurationUnknown` | `bool` | `true` if the official runtime has not yet been confirmed. |
| `synopsisShort` | `str` | Brief plot summary of the film. |
| `filmTitle` | `str` | Formatted display title of the film. |
| `hasSessions` | `bool` | `true` if screenings are currently scheduled/available to book. |
| `hasTrailer` | `bool` | `true` if a trailer is available for the film. |
| `embargoMessage` | `str \| null` | Restriction or pre-sale notice displayed before tickets go on general sale. |
| `embargoEndDate` | `str \| null` | ISO 8601 datetime string indicating when an active embargo lifts. |
| `embargoLevel` | `int \| str \| null` | Severity or tier of any booking/visibility embargo. |
| `priceMessage` | `str` | Custom pricing note or promotional message (empty string if none). |
| `alternativeCertificate` | `object` | Secondary/regional age rating object (values are `null` when unused). |
| `panelImageUrl` | `str` | URL to a wide/landscape promotional still used for banners or hero panels. |
| `filmStatus` | `int` | Numeric status code representing the film's release/booking state. |
| `trailers` | `list` | List of trailer media objects/links associated with the film. |
| `director` | `str` | Name of the film's director(s). |
| `distributor` | `str` | Film distributor name and territory. |
| `movieXchangeCode` | `str` | UUID identifier used by the MovieXchange film metadata service. |
| `crossCountryMovieXchangeId` | `str` | Cross-territory MovieXchange UUID linking the same film across regions. |
| `originalTitle` | `str` | Original release title before any regional formatting or translation. |
| `showingInCinemas` | `list<str>` | Array of `cinemaId` strings where the film is currently showing (matches `cinemaId` from the cinemas endpoint). |
| `genres` | `list<str>` | List of genre labels. |
| `sessionAttributes` | `list` | Screening-level format or feature tags available for this film. |

### Certificate Object Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `name` | `str \| null` | Short rating code. |
| `description` | `str \| null` | Official age-rating guidance text. |
| `src` | `str \| null` | URL to the rating badge icon. |


## Fetch List of Showtimes

Endpoints which return a list of showtimes.

### Endpoints

#### `GET https://www.myvue.com/api/microservice/showings/cinemas/{cinemaId}/films/{filmId}/showingGroups`

Retrieves all showings for a given film in a given cinema

- **Example Request:** `GET https://www.myvue.com/api/microservice/showings/cinemas/10051/films/HO00020283/showingGroups`

##### Parameters

| Parameter | Location | Type | Required | Description |
| :--- | :---- | :--- | :--- | :--- |
| `cinemaId` | Path | `str` | **Yes** | The unique ID of the cinema (matches `cinemaId` from the cinema endpoint). |
| `filmId` | Path | `str` | **Yes** | The unique ID of the film (matches `filmId` from the films endpoint). |


### Example Response

```json
{
    "result": [
        {
            "date": "2026-11-19T00:00:00",
            "datePrefix": "Today",
            "pricingTypes": [],
            "sessions": [
                {
                    "sessionId": "500477",
                    "bookingUrl": "/book-tickets/summary/10018/HO00020283/500477",
                    "formattedPrice": "£13.99",
                    "isPriceVisible": true,
                    "duration": 158,
                    "startTime": "2026-11-19T19:30:00",
                    "endTime": "2026-11-19T22:33:00",
                    "showTimeWithTimeZone": "2026-11-19T19:30:00+00:00",
                    "isSoldOut": false,
                    "color": null,
                    "isMidnightSession": false,
                    "isBookingAvailable": true,
                    "bookingAvailability": 0,
                    "attributes": [
                        {
                            "name": "English",
                            "shortName": "",
                            "value": "english",
                            "description": "Films shown in the English language",
                            "attributeType": "Language",
                            "color": "",
                            "borderGradient": [],
                            "backgroundImageUrl": null,
                            "iconName": null
                        },
                        {
                            "name": "Dolby Atmos",
                            "shortName": "Dolby Atmos",
                            "value": "atmos",
                            "description": "Screenings that use Dolby Atmos sound",
                            "attributeType": "Session",
                            "color": "",
                            "borderGradient": [],
                            "backgroundImageUrl": null,
                            "iconName": null
                        },
                        {
                            "name": "HDR by Barco",
                            "shortName": "HDR by Barco",
                            "value": "hdr",
                            "description": "High dynamic range (HDR) laser projectors giving more vivid colours and contrast.",
                            "attributeType": "Session",
                            "color": "",
                            "borderGradient": [],
                            "backgroundImageUrl": null,
                            "iconName": null
                        },
                        {
                            "name": "Biggest Screen",
                            "shortName": "Biggest Screen",
                            "value": "biggest-screen",
                            "description": "Biggest screen in venue.",
                            "attributeType": "Session",
                            "color": "",
                            "borderGradient": [],
                            "backgroundImageUrl": null,
                            "iconName": null
                        },
                        {
                            "name": "EPIC",
                            "shortName": "",
                            "value": "epic",
                            "description": "Our biggest screen with the latest in cinema technology to give you the best big screen experience.",
                            "attributeType": "Session",
                            "color": "",
                            "borderGradient": [
                                {
                                    "color": "4830B1",
                                    "fill": "20%"
                                },
                                {
                                    "color": "FB5004",
                                    "fill": "100%"
                                }
                            ],
                            "backgroundImageUrl": "https://www.myvue.com/-/media/vuecinemas/general-imagery/epic/20desktop3x.png?rev=b87042d2ebac410b8ee9ab3f9628cd65",
                            "iconName": null
                        },
                        {
                            "name": "Single Seat",
                            "shortName": "",
                            "value": "single-seat",
                            "description": "SingleSeat",
                            "attributeType": "Session",
                            "color": "",
                            "borderGradient": [],
                            "backgroundImageUrl": null,
                            "iconName": null
                        },
                        {
                            "name": "Ultra Lux and Lux",
                            "shortName": "Ultra Lux and Lux",
                            "value": "ultra-lux-and-lux",
                            "description": "This screen has Ultra Lux and Lux seating.",
                            "attributeType": "Session",
                            "color": "",
                            "borderGradient": [],
                            "backgroundImageUrl": null,
                            "iconName": null
                        }
                    ],
                    "screenName": "EPIC",
                    "sessionPricingDisplayStatus": 1,
                    "wheelchairSeatAvailability": 1
                }
            ]
        }
    ],
    "responseCode": 0,
    "errorMessage": null
}
```

### Top-Level Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `result` | `list` | List of date group objects |
| `responseCode` | `int` | `0` indicates success; non-zero indicates an error. |
| `errorMessage` | `str \| null` | Error details when `responseCode` is non-zero. |

### Date Group Object Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `date` | `str` | ISO 8601 datetime string for the screening day. |
| `datePrefix` | `str` | Relative or friendly day label (e.g., `"Today"`, `"Tomorrow"`, or `""`). |
| `pricingTypes` | `list` | Pricing tier metadata or filters associated with the day's screenings. |
| `sessions` | `list<object>` | List of individual screening/showtime objects occurring on this date. |

### Session Object Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `sessionId` | `str` | Unique identifier for the screening session. |
| `bookingUrl` | `str` | Relative path to the ticket booking flow. |
| `formattedPrice` | `str` | Display-ready ticket price string with currency symbol. |
| `isPriceVisible` | `bool` | `true` if ticket pricing should be shown in the UI. |
| `duration` | `int` | Screening duration in minutes (including ads). |
| `startTime` | `str` | ISO 8601 local start timestamp of the screening. |
| `endTime` | `str` | ISO 8601 local end timestamp of the screening. |
| `showTimeWithTimeZone` | `str` | ISO 8601 start timestamp including UTC offset. |
| `isSoldOut` | `bool` | `true` if no seats remain available for the session. |
| `color` | `str \| null` | Optional hex/theme color associated with the session or screen badge. |
| `isMidnightSession` | `bool` | `true` if the screening is a midnight or late-night special session. |
| `isBookingAvailable` | `bool` | `true` if tickets can currently be booked online. |
| `bookingAvailability` | `int` | Numeric availability/booking state code. |
| `attributes` | `list<object>` | Format, audio, seating, and language tags for this screening (see table below). |
| `screenName` | `str` | Name or format label of the auditorium/screen. |
| `sessionPricingDisplayStatus` | `int` | Numeric status controlling how session pricing is displayed. |
| `wheelchairSeatAvailability` | `int` | Indicator/code for wheelchair-accessible seating availability on this session. |

### Session Attribute Object Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `name` | `str` | Full label of the attribute (e.g., `"Dolby Atmos"`, `"English"`, `"EPIC"`). |
| `shortName` | `str` | Abbreviated label for compact badges (may be empty string `""`). |
| `value` | `str` | Normalized slug/identifier for the attribute (e.g., `"atmos"`, `"english"`, `"epic"`). |
| `description` | `str` | Human-readable explanation of the format, language, or seating feature. |
| `attributeType` | `str` | Category of the attribute (e.g., `"Language"`, `"Session"`). |
| `color` | `str` | Hex color code for UI styling (empty string `""` if unused). |
| `borderGradient` | `list<object>` | Gradient stop objects (`color` hex and `fill` percentage) used for styled badges like `EPIC`. |
| `backgroundImageUrl` | `str \| null` | URL to a badge/banner image for special formats (e.g., `EPIC`), or `null`. |
| `iconName` | `str \| null` | Icon identifier/name if rendered from an icon set, or `null`. |

### Gradient Stop Object Fields (`borderGradient` items)

| Field | Type | Description |
| :--- | :--- | :--- |
| `color` | `str` | Hex color value without leading `#` (e.g., `"4830B1"`, `"FB5004"`). |
| `fill` | `str` | Gradient stop position/percentage (e.g., `"20%"`, `"100%"`). |
