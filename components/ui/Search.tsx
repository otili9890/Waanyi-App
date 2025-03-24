import React, { Component, useState } from "react";
import { StyleSheet, Text, View, FlatList } from "react-native";
import { ListItem, SearchBar } from "react-native-elements";
import filter from "lodash.filter";

const DATA = require("../../assets/data/waanyi.json");

export default function Search () {
  const [searchQuery, setSearchQuery] = useState("");
  const [data, setData] = useState(DATA);
  const [fullData, setFullData] = useState(DATA);

  const searchFunction = (query) => {
    setSearchQuery(query);
    const formattedQuery = query.toLowerCase();
    const filteredData = filter(fullData, (item) => {
      return contains(item, formattedQuery);
    })
    setData(filteredData)
  };

  const processList = (obj) =>{
    if (obj instanceof Array && obj.length > 0) {
      let list = '';
      obj.forEach((e, idx) => {
        list += e;
        if (idx < obj.length - 1) {
          list += ', ';
        }
      });
      list += '.';
      return list;
    } else {
      return obj;
    }
  }

  const contains = ({id, English_Gloss}, query) => {
    console.log("Eng gloss is ", typeof English_Gloss);
    if (English_Gloss instanceof Array && English_Gloss.length > 0) {
      if (id.toLowerCase().includes(query) || English_Gloss.some((e) => e.toLowerCase().includes(query))) {
        return true;
      }
    } else if (English_Gloss instanceof String) {
      if (id.toLowerCase().includes(query) || English_Gloss.includes(query)) {
        return true;
      }
    }
    return false;
  }

  const Item = ({ id, gloss }) => {
    return (
      <ListItem style={styles.item}>
        <Text>{id}</Text>
        <Text>{gloss}</Text>
      </ListItem>
    );
  };
  
  const renderItem = ({ item }) => <Item id={item.id} gloss={processList(item.English_Gloss)} />;

  return (
    <View style={styles.container}>
      <SearchBar
        style={styles.search}
        placeholder="Search Here..."
        lightTheme
        clearButtonMode="always"
        round
        value={searchQuery}
        onChangeText={(text) => searchFunction(text)}
        autoCorrect={false}
      />
      <FlatList
        data={data}
        renderItem={renderItem}
        ListFooterComponent={() => <Text>Footer</Text>}
        keyExtractor={(item) => item.id}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: "red",
    marginTop: 30,
    padding: 2,
  },
  item: {
    color: "white",
    marginVertical: 8,
    marginHorizontal: 16,
  },
  search: {
    backgroundColor: "none",
  },
});
