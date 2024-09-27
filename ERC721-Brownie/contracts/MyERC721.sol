// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

contract MyERC721 is ERC721Enumerable, Ownable{
    uint256 public immutable TOTAL_SUPPLY;
    uint256 public immutable MAX_PER_MINT;
    uint256 public immutable MAX_PER_ADDRESS;
    uint256 public immutable MINT_PRICE;
    // uint256 public constant MAX_SUPPLY = 100;
    // uint256 public constant MAX_PER_MINT = 3;
    // uint256 public constant MAX_PER_ADDRESS = 6;
    // uint256 public constant MINT_PRICE = 0.001 ether;

    //mapping(address => uint256) public mintedTokens;
    
    string public _baseTokenURI;

    mapping(address => uint256) private mintedTokens;

    constructor(
        address initialOwner,
        uint256 maxSupply,
        uint256 maxPerMint,
        uint256 maxPerAddress,
        uint256 mintPrice
    ) ERC721("MyNFTCollection", "MNFT") Ownable(initialOwner) {
        TOTAL_SUPPLY = maxSupply;
        MAX_PER_MINT = maxPerMint;
        MAX_PER_ADDRESS = maxPerAddress;
        MINT_PRICE = mintPrice;
    }


    // Устанавливаем базовый URI для метаданных
    function setBaseURI(string memory baseTokenURI) external onlyOwner {
        _baseTokenURI = baseTokenURI;
    }

    // Переопределяем _baseURI для поддержки базового URI
    function _baseURI() internal view virtual override returns (string memory) {
        return _baseTokenURI;
    }

    // Переопределяем tokenURI для возвращения полного URI метаданных для токена
    function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
        // require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token");

        // В этом примере возвращаем базовый URI + tokenId + ".json"
        return string(abi.encodePacked(_baseTokenURI, Strings.toString(tokenId), ".json"));
    }


    function getMintedTokens(address owner) external view returns (uint256) {
        return mintedTokens[owner];
    }
    

    function mint(uint256 amount) public payable {
        require(amount > 0 && amount <= MAX_PER_MINT, "Invalid mint amount");
        require(totalSupply() + amount <= TOTAL_SUPPLY, "Max supply exceeded");
        require(mintedTokens[msg.sender] + amount <= MAX_PER_ADDRESS, "Max tokens per address exceeded");
        require(msg.value == MINT_PRICE * amount, "Incorrect Ether sent");

        for (uint256 i = 0; i < amount; i++) {
            uint256 tokenId = totalSupply();
            mintedTokens[msg.sender]++;
            _safeMint(msg.sender, tokenId);
        }
    }


    function withdraw(uint256 amount, address payable to) external onlyOwner {
        require(amount <= address(this).balance, "Insufficient balance");
        to.transfer(amount);
    }

}

