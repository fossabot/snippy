-- database.sql

-- Schema for Snippy application.

-- Snips are short command examples.
create table if not exists snip (
    id          integer primary key,
    snip        text not null unique,
    metadata    text default '',
    tags        text default '',
    comment     text default ''
);

-- Logs are troubleshooting reference notes.
create table if not exists log (
    id          integer primary key,
    log         text not null unique,
    metadata    text default '',
    tags        text default '',
    comment     text default ''
);
