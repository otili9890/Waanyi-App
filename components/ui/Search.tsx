import React, { Component } from "react";
import { StyleSheet, Text, View, FlatList } from "react-native";
import { ListItem, SearchBar } from "react-native-elements";

const DATA = require("../../assets/data/waanyi.json");

const Item = ({ id, gloss }) => {
  return (
    <ListItem style={styles.item}>
      <Text>{id}</Text>
      <Text>{gloss}</Text>
    </ListItem>
  );
};

const renderItem = ({ item }) => <Item id={item.id} gloss={item.English_Gloss} />;
class Search extends Component {
  constructor(props) {
    super(props); 
    this.state = {
      loading: false,
      data: DATA,
      error: null,
      searchValue: "",
    };
    this.arrayholder = DATA;
  }

  searchFunction = (text) => {
    const updatedData = this.arrayholder.filter((item) => {
      console.log("Gloss: ", item.English_Gloss);
      var item_data = '';
      var item_gloss = '';
      if (item.id) {
        item_data = `${item.id.toUpperCase()})`;
      } if (item.English_Gloss) {
        item_gloss = `${item.English_Gloss[0].toUpperCase()}`;
      }
        
      const text_data = text.toUpperCase();
      return item_data.indexOf(text_data) > -1 || item_gloss.indexOf(text_data) > -1;
      }
    );
    this.setState({ data: updatedData, searchValue: text });
  };

  render() {
    return (
      <View style={styles.container}>
        <SearchBar
          style={styles.search}
          placeholder="Search Here..."
          lightTheme
          clearButtonMode="always"
          round
          value={this.state.searchValue}
          onChangeText={(text) => this.searchFunction(text)}
          autoCorrect={false}
        />
        <FlatList
          data={this.state.data}
          renderItem={renderItem}
          ListFooterComponent={() => <Text>Footer</Text>}
          keyExtractor={(item) => item.id}
        />
      </View>
    );
  }
}

export default Search;

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
